"""
Academic database search functions for the literature search stage.

Active databases:
  • arXiv            — REST API (free, no auth)
  • Semantic Scholar — covers ACM, SSRN, and broad scholarly indexes (1 req/s with key)
  • CrossRef         — broad journal/conference coverage (free, no auth)
  • OSF / SHARE      — social-science preprints (free, no auth)
  • PubMed           — biomedical / clinical literature (free, no auth)
  • Elsevier (Scopus) — broad multi-publisher bibliographic index (requires API key)
"""

import io
import json
import time
import logging
import re
import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable, List, Dict, Optional

logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv
from config import (
    MAX_PAPERS_PER_QUERY,
    DEEP_RESEARCH_MAX_TOOL_CALLS,
    DEEP_RESEARCH_MODEL,
    DEEP_RESEARCH_TIMEOUT_SECONDS,
    ENABLED_SEARCH_DATABASES,
    KEENABLE_API_KEY,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
)
load_dotenv()

_SS_API_KEY   = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
_OSF_TOKEN    = os.getenv("OSF_TOKEN", "")
_NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")
_ELS_API_KEY  = os.getenv("ELSEVIER_API_KEY", "")
_WOS_API_KEY  = os.getenv("WOS_API_KEY", "")
_HEADERS      = {"User-Agent": "MetaAnalysisPipeline/1.0 (academic research)"}
_SS_HEADERS   = {**_HEADERS, **({"x-api-key": _SS_API_KEY} if _SS_API_KEY else {})}
_OSF_HEADERS  = {**_HEADERS, **({"Authorization": f"Bearer {_OSF_TOKEN}"} if _OSF_TOKEN else {})}
_ELS_HEADERS  = {**_HEADERS, "Accept": "application/json",
                  **({"X-ELS-APIKey": _ELS_API_KEY} if _ELS_API_KEY else {})}
_WOS_HEADERS  = {**_HEADERS, "Accept": "application/json",
                  **({"X-ApiKey": _WOS_API_KEY} if _WOS_API_KEY else {})}
_TIMEOUT = 25

# arXiv: polite crawling policy — no more than 1 request every 3 seconds
_ARXIV_DELAY = 3.0
# Semantic Scholar: 1 req/s with key
_SS_DELAY = 1.1 if _SS_API_KEY else 0
# NCBI: 10 req/s with key, 3 req/s without
_NCBI_DELAY = 0.11 if _NCBI_API_KEY else 0.35

# OSF preprint providers to search — broad cross-disciplinary set
_OSF_PROVIDERS = [
    "psyarxiv",    # psychology, cognitive science, neuroscience
    "socarxiv",    # social science, economics, political science
    "osf",         # general OSF preprints
    "edarxiv",     # education
    "mindrxiv",    # mindfulness, contemplative research
    "metaarxiv",   # meta-science, open science
    "sportrxiv",   # sport, exercise, health
    "engrxiv",     # engineering
    "eartharxiv",  # earth & environmental science
    "ecoevorxiv",  # ecology, evolution
]


# ── OpenRouter Deep Research paper finder ─────────────────────────────────────

def _json_from_model_text(text: str) -> Optional[dict]:
    """Parse JSON from raw model text, including fenced JSON blocks."""
    if not text:
        return None
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None


def _parse_deep_research_papers(text: str, max_results: int) -> List[Dict]:
    """Convert Deep Research JSON output into pipeline paper dictionaries."""
    payload = _json_from_model_text(text) or {}
    items = payload.get("papers") if isinstance(payload, dict) else []
    if not isinstance(items, list):
        return []

    papers: List[Dict] = []
    for item in items[:max_results]:
        if not isinstance(item, dict):
            continue
        title = (item.get("title") or "").strip()
        if not title:
            continue
        year = item.get("year") or 0
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = 0
        url = (item.get("url") or item.get("landing_page_url") or "").strip()
        pdf_url = (item.get("pdf_url") or item.get("open_access_pdf") or "").strip() or None
        doi = (item.get("doi") or "").strip() or None
        papers.append({
            "id": item.get("id") or f"deep_research:{abs(hash((title, url))) % 10_000_000}",
            "title": title,
            "abstract": (item.get("abstract") or item.get("summary") or "").strip(),
            "authors": item.get("authors") or [],
            "year": year,
            "url": url,
            "source": "deep_research",
            "open_access_pdf": pdf_url,
            "doi": doi,
        })
    return papers


def search_deep_research(query: str, max_results: int = MAX_PAPERS_PER_QUERY,
                         start_year: int = 2020) -> List[Dict]:
    """Use OpenRouter-hosted Deep Research as an additional relevant-paper finder."""
    if not OPENROUTER_API_KEY:
        logger.warning("[DeepResearch] OPENROUTER_API_KEY not set -- skipping Deep Research search.")
        return []

    try:
        from openai import OpenAI
    except ImportError:
        logger.warning("[DeepResearch] openai package not installed -- skipping Deep Research search.")
        return []

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        # A negative value means "no limit" (same convention as
        # FULL_TEXT_FETCH_BUDGET) -- timeout=None tells the underlying httpx
        # client to disable the request timeout entirely.
        timeout=DEEP_RESEARCH_TIMEOUT_SECONDS if DEEP_RESEARCH_TIMEOUT_SECONDS >= 0 else None,
    )
    prompt = (
        "Find relevant empirical research papers for a meta-analysis.\n"
        f"Search query: {query}\n"
        f"Earliest publication year: {start_year}\n\n"
        "Prioritize original empirical studies with quantitative outcomes. "
        "Prefer open-access papers and include arXiv URLs or PDF URLs when available. "
        "Do not return reviews, editorials, or opinion pieces unless no empirical papers exist.\n\n"
        "Return only valid JSON in this exact schema:\n"
        "{\n"
        '  "papers": [\n'
        "    {\n"
        '      "title": "string",\n'
        '      "authors": ["string"],\n'
        '      "year": 2024,\n'
        '      "url": "https://...",\n'
        '      "pdf_url": "https://... or empty string",\n'
        '      "doi": "string or empty string",\n'
        '      "abstract": "short evidence-focused summary"\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    # A negative value means "no limit" (same convention as FULL_TEXT_FETCH_BUDGET)
    # -- omitting max_tool_calls entirely lets the model keep calling tools
    # until it decides to stop, instead of capping it.
    create_kwargs = dict(
        model=DEEP_RESEARCH_MODEL,
        input=prompt,
        tools=[{"type": "openrouter:web_search"}],
    )
    if DEEP_RESEARCH_MAX_TOOL_CALLS >= 0:
        create_kwargs["max_tool_calls"] = DEEP_RESEARCH_MAX_TOOL_CALLS

    try:
        response = client.responses.create(**create_kwargs)
    except Exception as exc:
        logger.warning(f"[DeepResearch] Request failed: {exc}")
        return []

    output_text = getattr(response, "output_text", "") or str(response)
    papers = _parse_deep_research_papers(output_text, max_results)
    logger.info(f"[DeepResearch] {len(papers)} papers for: {query!r}")
    return papers


def _get_with_retry(url: str, params: dict = None, headers: dict = None,
                    max_retries: int = 3) -> requests.Response:
    """GET with exponential back-off on 429 / 5xx responses."""
    h = headers or _HEADERS
    for attempt in range(max_retries):
        resp = requests.get(url, params=params, headers=h, timeout=_TIMEOUT)
        if resp.status_code == 429:
            wait = 2 ** attempt * 5
            logger.info(f"Rate-limited by {url[:50]} -- waiting {wait}s")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
    return resp


# ── arXiv ─────────────────────────────────────────────────────────────────────

def search_arxiv(query: str, max_results: int = 50,
                 start_year: int = 2020) -> List[Dict]:
    """Search arXiv via their Atom REST API."""
    time.sleep(_ARXIV_DELAY)  # arXiv polite-crawling policy: ≤1 req/3 s
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    try:
        resp = _get_with_retry(url, params)
    except Exception as exc:
        logger.warning(f"[arXiv] Request failed: {exc}")
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(resp.text)
    papers = []
    for entry in root.findall("atom:entry", ns):
        try:
            year_str = (entry.findtext("atom:published", "", ns) or "")[:4]
            year = int(year_str) if year_str.isdigit() else 0
            if year < start_year:
                continue
            arxiv_id = (entry.findtext("atom:id", "", ns) or "").split("/abs/")[-1]
            authors = [a.findtext("atom:name", "", ns)
                       for a in entry.findall("atom:author", ns)]
            papers.append({
                "id": f"arxiv:{arxiv_id}",
                "title": (entry.findtext("atom:title", "", ns) or "").strip().replace("\n", " "),
                "abstract": (entry.findtext("atom:summary", "", ns) or "").strip().replace("\n", " "),
                "authors": authors,
                "year": year,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "source": "arxiv",
                "open_access_pdf": f"https://arxiv.org/pdf/{arxiv_id}",
            })
        except Exception:
            continue

    logger.info(f"[arXiv] {len(papers)} papers for: {query!r}")
    return papers


# ── Semantic Scholar ───────────────────────────────────────────────────────────

def search_semantic_scholar(query: str, max_results: int = 50,
                             start_year: int = 2020) -> List[Dict]:
    """
    Search Semantic Scholar Graph API.
    With API key: 1 req/s. Without: ~100 req/5min.
    Covers ACM DL, SSRN, Web-of-Science-indexed journals, PubMed, and more.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": min(max_results, 100),
        "fields": "title,abstract,authors,year,externalIds,venue,openAccessPdf",
        "year": f"{start_year}-",
    }
    try:
        for attempt in range(5):
            if _SS_DELAY:
                time.sleep(_SS_DELAY)
            r = requests.get(url, params=params, headers=_SS_HEADERS, timeout=_TIMEOUT)
            if r.status_code == 429:
                wait = 2 ** attempt * 10
                logger.info(f"[SemanticScholar] Rate-limited, waiting {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            break
        else:
            logger.warning("[SemanticScholar] Exceeded retries.")
            return []
    except Exception as exc:
        logger.warning(f"[SemanticScholar] Request failed: {exc}")
        return []

    papers = []
    for item in data.get("data", []):
        try:
            year = item.get("year") or 0
            if year < start_year:
                continue
            ext = item.get("externalIds") or {}
            doi = ext.get("DOI", "")
            arxiv_id = ext.get("ArXiv", "")
            acm_id = ext.get("ACM", "")
            ssrn_id = ext.get("SSRN", "")
            venue = (item.get("venue") or "").lower()
            if acm_id or "acm" in venue:
                source = "acm"
            elif ssrn_id or "ssrn" in venue:
                source = "ssrn"
            elif arxiv_id:
                source = "arxiv"
            else:
                source = "semantic_scholar"
            url_str = (
                f"https://doi.org/{doi}" if doi
                else f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id
                else f"https://www.semanticscholar.org/paper/{item.get('paperId', '')}"
            )
            oa = item.get("openAccessPdf") or {}
            open_access_pdf = (
                f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id
                else oa.get("url")
            )
            papers.append({
                "id": f"ss:{item.get('paperId', '')}",
                "title": item.get("title", "").strip(),
                "abstract": (item.get("abstract") or "").strip(),
                "authors": [a.get("name", "") for a in (item.get("authors") or [])],
                "year": year,
                "url": url_str,
                "source": source,
                "open_access_pdf": open_access_pdf,
                "doi": doi,
            })
        except Exception:
            continue

    logger.info(f"[SemanticScholar] {len(papers)} papers for: {query!r}")
    return papers


# ── CrossRef ──────────────────────────────────────────────────────────────────

def search_crossref(query: str, max_results: int = 50,
                    start_year: int = 2020) -> List[Dict]:
    """
    Search CrossRef -- covers Springer, Elsevier, Wiley, ACM journals.
    Free, no authentication required.
    """
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": min(max_results, 100),
        "filter": f"from-pub-date:{start_year}",
        "select": "DOI,title,abstract,author,published,container-title",
        "sort": "relevance",
    }
    try:
        resp = _get_with_retry(url, params)
        data = resp.json()
    except Exception as exc:
        logger.warning(f"[CrossRef] Request failed: {exc}")
        return []

    papers = []
    for item in data.get("message", {}).get("items", []):
        try:
            pub = item.get("published", {})
            parts = pub.get("date-parts", [[0]])[0]
            year = int(parts[0]) if parts else 0
            if year < start_year:
                continue
            titles = item.get("title", [])
            title = titles[0].strip() if titles else ""
            if not title:
                continue
            doi = item.get("DOI", "")
            abstract = item.get("abstract", "").strip()
            abstract = abstract.replace("<jats:p>", "").replace("</jats:p>", "")
            authors = [
                f"{a.get('family', '')} {a.get('given', '')}".strip()
                for a in item.get("author", [])
            ]
            container = (item.get("container-title") or [""])[0].lower()
            source = "acm" if ("acm" in container or "proceedings" in container) else "crossref"
            papers.append({
                "id": f"cr:{doi.replace('/', '_')}",
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "year": year,
                "url": f"https://doi.org/{doi}" if doi else "",
                "source": source,
                "doi": doi,
            })
        except Exception:
            continue

    logger.info(f"[CrossRef] {len(papers)} papers for: {query!r}")
    return papers


# ── OSF Preprints (API v2, authenticated) ─────────────────────────────────────

def _search_osf_provider(provider_id: str, keyword: str,
                          max_results: int, start_year: int) -> List[Dict]:
    """Search a single OSF preprint provider by title keyword."""
    url = f"https://api.osf.io/v2/providers/preprints/{provider_id}/preprints/"
    params = {
        "filter[title]": keyword,
        "page[size]": min(max_results, 100),
        "sort": "-date_created",
    }
    try:
        resp = requests.get(url, params=params, headers=_OSF_HEADERS, timeout=_TIMEOUT)
        if resp.status_code == 404:
            return []       # provider not available
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.debug(f"[OSF] provider={provider_id} failed: {exc}")
        return []

    papers = []
    for item in data.get("data", []):
        try:
            attrs = item.get("attributes", {})
            date_str = attrs.get("date_published") or attrs.get("date_created") or ""
            year = int(date_str[:4]) if len(date_str) >= 4 and date_str[:4].isdigit() else 0
            if year < start_year:
                continue
            doi = attrs.get("doi", "") or ""
            osf_id = item.get("id", "")
            url_str = (f"https://doi.org/{doi}" if doi
                       else f"https://osf.io/{osf_id}/")
            title = attrs.get("title", "").strip()
            if not title:
                continue
            # OSF preprint primary file download link
            links = item.get("links") or {}
            preprint_doi = attrs.get("doi") or ""
            # relationships → primary_file → links → download
            rels = item.get("relationships") or {}
            primary_file = rels.get("primary_file") or {}
            pf_links = primary_file.get("links") or {}
            osf_pdf_url = pf_links.get("related", {}).get("href") if isinstance(pf_links.get("related"), dict) else None
            if not osf_pdf_url:
                osf_pdf_url = links.get("preprint_doi") or None
            papers.append({
                "id": f"osf:{osf_id}",
                "title": title,
                "abstract": attrs.get("description", "").strip(),
                "authors": [],
                "year": year,
                "url": url_str,
                "source": "osf",
                "open_access_pdf": osf_pdf_url,
                "doi": preprint_doi,
            })
        except Exception:
            continue
    return papers


def search_osf(query: str, max_results: int = 30,
               start_year: int = 2020) -> List[Dict]:
    """
    Search OSF preprints across multiple providers using the OSF API v2.
    Requires OSF_TOKEN in .env for authenticated access.
    Searches psyarxiv, socarxiv, osf, edarxiv, mindrxiv, metaarxiv, and more.
    """
    if not _OSF_TOKEN:
        logger.warning("[OSF] No OSF_TOKEN set -- skipping OSF search.")
        return []

    # Use the first keyword from the query for title filtering
    keyword = query.split()[:4]
    keyword_str = " ".join(keyword)

    all_papers: List[Dict] = []
    per_provider = max(1, max_results // len(_OSF_PROVIDERS))

    for provider_id in _OSF_PROVIDERS:
        papers = _search_osf_provider(provider_id, keyword_str, per_provider, start_year)
        all_papers.extend(papers)
        if papers:
            logger.debug(f"[OSF] {provider_id}: {len(papers)} papers")
        if all_papers and max_results == 1:
            break  # one result found — stop early

    # Deduplicate within OSF results
    seen, unique = set(), []
    for p in all_papers:
        key = p["title"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(p)

    logger.info(f"[OSF] {len(unique)} unique preprints for: {query!r}")
    return unique[:max_results]


# ── PubMed ────────────────────────────────────────────────────────────────────

def search_pubmed(query: str, max_results: int = 50,
                  start_year: int = 2020) -> List[Dict]:
    """
    Search PubMed via NCBI E-utilities.
    With NCBI_API_KEY: up to 10 req/s. Without: up to 3 req/s.
    """
    # Step 1: search for IDs
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": f"{query} AND {start_year}:{2030}[pdat]",
        "retmax": min(max_results, 200),
        "retmode": "json",
        "sort": "relevance",
    }
    if _NCBI_API_KEY:
        search_params["api_key"] = _NCBI_API_KEY
    try:
        resp = _get_with_retry(search_url, search_params)
        ids = resp.json().get("esearchresult", {}).get("idlist", [])
    except Exception as exc:
        logger.warning(f"[PubMed] Search failed: {exc}")
        return []

    if not ids:
        logger.info(f"[PubMed] 0 results for: {query!r}")
        return []

    # Step 2: fetch summaries for those IDs
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml",
        "rettype": "abstract",
    }
    if _NCBI_API_KEY:
        fetch_params["api_key"] = _NCBI_API_KEY
    try:
        time.sleep(_NCBI_DELAY)
        resp = _get_with_retry(fetch_url, fetch_params)
        root = ET.fromstring(resp.text)
    except Exception as exc:
        logger.warning(f"[PubMed] Fetch failed: {exc}")
        return []

    papers = []
    for article in root.findall(".//PubmedArticle"):
        try:
            pmid_el = article.find(".//PMID")
            pmid = pmid_el.text if pmid_el is not None else ""

            title_el = article.find(".//ArticleTitle")
            title = (title_el.text or "").strip() if title_el is not None else ""
            if not title:
                continue

            abstract_parts = article.findall(".//AbstractText")
            abstract = " ".join(
                (el.text or "") for el in abstract_parts if el.text
            ).strip()

            # Publication year
            year_el = article.find(".//PubDate/Year")
            medline_el = article.find(".//MedlineDate")
            if year_el is not None and year_el.text:
                year = int(year_el.text)
            elif medline_el is not None and medline_el.text:
                year = int(medline_el.text[:4])
            else:
                year = 0
            if year < start_year:
                continue

            authors = []
            for auth in article.findall(".//Author"):
                last = (auth.findtext("LastName") or "").strip()
                fore = (auth.findtext("ForeName") or "").strip()
                if last:
                    authors.append(f"{last} {fore}".strip())

            doi_el = article.find(".//ArticleId[@IdType='doi']")
            doi = doi_el.text.strip() if doi_el is not None else ""
            url_str = f"https://doi.org/{doi}" if doi else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            papers.append({
                "id": f"pubmed:{pmid}",
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "year": year,
                "url": url_str,
                "source": "pubmed",
                "doi": doi,
                "pmid": pmid,
            })
        except Exception:
            continue

    logger.info(f"[PubMed] {len(papers)} papers for: {query!r}")
    return papers


# ── Keenable (general web search + landing-page extraction) ────────────────────
# https://keenable.ai -- NOT an academic index. A general-purpose web-search
# API used here as an additional (not sole) full-text discovery source in
# agents/paper_reading_agent.py::fetch_fulltext_node, where its candidate
# URLs are merged, validated (_metadata_hit_matches_paper), and deduplicated
# alongside arXiv/Semantic Scholar/CrossRef/OSF/PubMed/Deep Research hits --
# not tried only as a last-resort fallback after everything else fails.

_KEENABLE_SEARCH_URL = "https://api.keenable.ai/v1/search"
_KEENABLE_FETCH_URL = "https://api.keenable.ai/v1/fetch"


def _keenable_headers() -> dict:
    return {**_HEADERS, "Content-Type": "application/json", "X-API-Key": KEENABLE_API_KEY}


def _keenable_is_probable_pdf_url(url: str) -> bool:
    """Lightweight standalone check (mirrors agents/paper_reading_agent.py's
    _is_probable_pdf_url) -- not imported from there to avoid a circular
    import, since that module already imports FROM this one."""
    path = (url or "").split("?", 1)[0].lower()
    return path.endswith(".pdf") or "/pdf/" in path or path.endswith("/pdf")


def search_keenable(query: str, max_results: int = 10,
                     start_year: int = 2020) -> List[Dict]:
    """General web search via Keenable. No key => no-op (returns []), same
    convention as every other optional source above."""
    if not KEENABLE_API_KEY:
        return []

    body = {"query": query, "max_results": max(1, min(max_results, 50))}
    if start_year and start_year > 1900:
        body["published_after"] = f"{start_year}-01-01"

    try:
        for attempt in range(3):
            resp = requests.post(_KEENABLE_SEARCH_URL, json=body,
                                  headers=_keenable_headers(), timeout=_TIMEOUT)
            if resp.status_code == 429:
                wait = 2 ** attempt * 5
                logger.info(f"[Keenable] Rate-limited -- waiting {wait}s")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            break
        else:
            logger.warning("[Keenable] Exceeded retries.")
            return []
    except Exception as exc:
        logger.warning(f"[Keenable] Search request failed: {exc}")
        return []

    papers = []
    for item in (data.get("results") or [])[:max_results]:
        try:
            url = (item.get("url") or "").strip()
            title = (item.get("title") or "").strip()
            if not url or not title:
                continue
            published = (item.get("published_at") or "")[:4]
            year = int(published) if published.isdigit() else 0
            papers.append({
                "id": f"keenable:{abs(hash(url)) % 10_000_000}",
                "title": title,
                "abstract": (item.get("description") or item.get("snippet") or "").strip(),
                "authors": [],
                "year": year,
                "url": url,
                "source": "keenable",
                # Keenable indexes/ranks general web pages, not confirmed
                # PDFs -- only populate this when the URL itself already
                # looks like a direct PDF link (mirrors how the structured
                # academic connectors above set this field); otherwise
                # downstream code resolves the actual full text via the
                # normal returned-URL / landing-page strategies, including
                # keenable_fetch_markdown() below.
                "open_access_pdf": url if _keenable_is_probable_pdf_url(url) else None,
            })
        except Exception:
            continue

    logger.info(f"[Keenable] {len(papers)} results for: {query!r}")
    return papers


def keenable_fetch_markdown(url: str, max_chars: int = 120_000) -> Optional[str]:
    """Extract a URL's content as clean markdown via Keenable's /v1/fetch --
    a lighter-weight alternative to full browser automation (no headless
    Chromium): one HTTP call instead of a Playwright render. No key => None."""
    if not KEENABLE_API_KEY or not url:
        return None
    try:
        resp = requests.get(
            _KEENABLE_FETCH_URL,
            params={"url": url, "live": "true", "max_chars": max_chars},
            headers=_keenable_headers(),
            timeout=45,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.debug(f"[Keenable] Fetch failed for {url}: {exc}")
        return None
    content = (data.get("content") or "").strip()
    return content or None


# ── Elsevier (Scopus) ───────────────────────────────────────────────────────────

def search_scopus(query: str, max_results: int = 50,
                  start_year: int = 2020) -> List[Dict]:
    """
    Search Elsevier's Scopus Search API.
    Requires ELSEVIER_API_KEY (from https://dev.elsevier.com/) in .env.

    Uses the default STANDARD view -- requesting view=COMPLETE fails the
    entire request with 401 AUTHORIZATION_ERROR unless the key has an
    institutional Scopus entitlement from the calling IP (confirmed against
    the live API: COMPLETE gets rejected outright, not just missing fields).
    STANDARD view doesn't include the abstract ("dc:description") either, so
    title/authors/venue/year/DOI/URL are populated but abstract is not.
    """
    if not _ELS_API_KEY:
        logger.warning("[Scopus] No ELSEVIER_API_KEY set -- skipping Elsevier search.")
        return []

    url = "https://api.elsevier.com/content/search/scopus"
    params = {
        "query": f"TITLE-ABS-KEY({query})",
        "date": f"{start_year}-2030",
        "count": min(max_results, 200),
    }
    try:
        resp = _get_with_retry(url, params, headers=_ELS_HEADERS)
        entries = resp.json().get("search-results", {}).get("entry", [])
    except Exception as exc:
        logger.warning(f"[Scopus] Request failed: {exc}")
        return []

    papers = []
    for item in entries:
        try:
            title = (item.get("dc:title") or "").strip()
            if not title:
                continue

            cover_date = item.get("prism:coverDate") or ""
            year = int(cover_date[:4]) if cover_date[:4].isdigit() else 0
            if year < start_year:
                continue

            authors = [
                a.get("authname", "").strip()
                for a in (item.get("author") or [])
                if a.get("authname")
            ]
            if not authors and item.get("dc:creator"):
                authors = [item["dc:creator"].strip()]

            doi = (item.get("prism:doi") or "").strip()
            eid = item.get("eid", "")
            url_str = (
                f"https://doi.org/{doi}" if doi
                else f"https://www.scopus.com/record/display.uri?eid={eid}&origin=inward" if eid
                else ""
            )

            papers.append({
                "id": f"scopus:{eid or item.get('dc:identifier', '')}",
                "title": title,
                "abstract": (item.get("dc:description") or "").strip(),
                "authors": authors,
                "year": year,
                "url": url_str,
                "source": "elsevier",
                "doi": doi,
            })
        except Exception:
            continue

    logger.info(f"[Scopus] {len(papers)} papers for: {query!r}")
    return papers


# ── Web of Science (Clarivate "Starter" API) ─────────────────────────────────

def search_wos(query: str, max_results: int = 50,
               start_year: int = 2020) -> List[Dict]:
    """
    Search Web of Science via Clarivate's "wos-starter" API.
    Requires WOS_API_KEY (from https://developer.clarivate.com/) in .env.

    Confirmed LIVE and working (2026-08-12 -- see database_search.py's test
    suite): returns real hits with title/authors/year/DOI/PMID. No abstract
    field at this API tier (same limitation Scopus's STANDARD view has) --
    title/authors/venue/year/DOI/PMID are populated, abstract is not.
    Year filtering is done client-side after fetch (the Starter API's query
    language for date ranges wasn't confirmed against the live API, so this
    follows the same safe pattern already used by search_semantic_scholar).
    """
    if not _WOS_API_KEY:
        logger.warning("[WebOfScience] No WOS_API_KEY set -- skipping Web of Science search.")
        return []

    url = "https://api.clarivate.com/apis/wos-starter/v1/documents"
    params = {"q": f"TI=({query})", "limit": min(max_results, 50)}
    try:
        resp = _get_with_retry(url, params, headers=_WOS_HEADERS)
        hits = resp.json().get("hits", [])
    except Exception as exc:
        logger.warning(f"[WebOfScience] Request failed: {exc}")
        return []

    papers = []
    for item in hits:
        try:
            title = (item.get("title") or "").strip()
            if not title:
                continue
            source = item.get("source") or {}
            year = source.get("publishYear") or 0
            if year < start_year:
                continue
            authors = [
                a.get("displayName", "").strip()
                for a in (item.get("names", {}).get("authors") or [])
                if a.get("displayName")
            ]
            ident = item.get("identifiers") or {}
            doi = ident.get("doi", "") or ""
            pmid = ident.get("pmid") or None
            uid = item.get("uid", "")
            links = item.get("links") or {}
            url_str = f"https://doi.org/{doi}" if doi else (links.get("record") or "")

            papers.append({
                "id": f"wos:{uid}",
                "title": title,
                "abstract": "",  # not available at this API tier
                "authors": authors,
                "year": year,
                "url": url_str,
                "source": "wos",
                "doi": doi,
                "pmid": pmid,
            })
        except Exception:
            continue

    logger.info(f"[WebOfScience] {len(papers)} papers for: {query!r}")
    return papers


# ── ClinicalTrials.gov (public API, no key required) ─────────────────────────

def search_clinicaltrials_gov(query: str, max_results: int = 50,
                               start_year: int = 2020) -> List[Dict]:
    """
    Search ClinicalTrials.gov's public API v2 -- free, no API key.

    This is a TRIAL REGISTRY, not a paper database: entries are registered
    trials, not journal articles. Returns the registry's brief summary as
    the closest equivalent to an abstract, and preserves the NCT ID as
    `trial_registry_id` (see models.py::PaperRecord). When the registry
    entry cites a linked publication (PMID), that's returned too -- the
    existing PMID-based full-text cascade can then try to fetch it exactly
    as it does for a PubMed-sourced record, with no special-casing needed.
    No PDF/full-text is ever returned directly by this source (registries
    don't host full text) -- see this design's §6.
    """
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.term": query,
        "pageSize": min(max_results, 100),
        "fields": ",".join([
            "NCTId", "BriefTitle", "OfficialTitle", "BriefSummary",
            "Condition", "InterventionName", "StartDate", "OverallStatus",
            "ReferencePMID", "LeadSponsorName",
        ]),
    }
    try:
        resp = requests.get(url, params=params, headers=_HEADERS, timeout=_TIMEOUT)
        resp.raise_for_status()
        studies = resp.json().get("studies", [])
    except Exception as exc:
        logger.warning(f"[ClinicalTrials.gov] Request failed: {exc}")
        return []

    papers = []
    for study in studies:
        try:
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            nct_id = ident.get("nctId", "")
            title = (ident.get("officialTitle") or ident.get("briefTitle") or "").strip()
            if not title:
                continue

            status_mod = protocol.get("statusModule", {})
            start_date = (status_mod.get("startDateStruct", {}) or {}).get("date", "") or ""
            year = int(start_date[:4]) if start_date[:4].isdigit() else 0
            if year and year < start_year:
                continue

            desc = protocol.get("descriptionModule", {})
            summary = (desc.get("briefSummary") or "").strip()

            refs_mod = protocol.get("referencesModule", {})
            pmids = [
                r.get("pmid") for r in (refs_mod.get("references") or [])
                if r.get("pmid")
            ]
            pmid = pmids[0] if pmids else None

            papers.append({
                "id": f"nct:{nct_id}",
                "title": title,
                "abstract": summary,
                "authors": [],  # trial registries don't list authors the way papers do
                "year": year,
                "url": f"https://clinicaltrials.gov/study/{nct_id}" if nct_id else "",
                "source": "clinicaltrials_gov",
                "doi": None,
                "pmid": pmid,
                "trial_registry_id": nct_id or None,
            })
        except Exception:
            continue

    logger.info(f"[ClinicalTrials.gov] {len(papers)} trial record(s) for: {query!r}")
    return papers


# ── Clean adapter placeholders -- CENTRAL / Embase / CINAHL ─────────────────
#
# NOT implemented against guessed APIs, per explicit instruction. Each of
# these needs either confirmed API documentation (CENTRAL/Cochrane) or a
# confirmed paid API entitlement (Embase, CINAHL -- see the conversation
# this design came from: Embase's API is explicitly excluded from
# Elsevier's free academic tier; CINAHL/EBSCO needs a separate EDS API
# agreement). Registered in SOURCE_REGISTRY as access_mode="unavailable"
# so status reporting is honest (never silently "enabled but does
# nothing" -- see §11 of the design / _normalize_db_name below). Until
# real credentials/docs exist, use utils/manual_import.py to bring in
# search results exported from these databases' own web interfaces --
# manual import already gets full pipeline treatment, no special-casing.

def search_central(query: str, max_results: int = 50, start_year: int = 2020) -> List[Dict]:
    """Placeholder -- CENTRAL/Cochrane API access/documentation not yet
    confirmed. See datapackage/RM5 backends (cochrane_benchmark/sources/
    structured/) for the UNRELATED, already-implemented job of fetching a
    *specific* Cochrane review's own text/data -- this function is about
    querying CENTRAL as a general primary-study search source, which is a
    different, not-yet-available capability."""
    logger.warning(
        "[CENTRAL] Not implemented -- no confirmed Cochrane/CENTRAL API access or "
        "documentation. Use utils/manual_import.py with an exported CENTRAL search "
        "instead."
    )
    return []


def search_embase(query: str, max_results: int = 50, start_year: int = 2020) -> List[Dict]:
    """Placeholder -- Embase's API is a separate, paid entitlement from
    Elsevier's free academic tier (confirmed), distinct from the Scopus
    access ELSEVIER_API_KEY already grants."""
    logger.warning(
        "[Embase] Not implemented -- Embase API requires a separate paid Elsevier "
        "entitlement, not covered by ELSEVIER_API_KEY. Use utils/manual_import.py "
        "with an exported Embase search instead."
    )
    return []


def search_cinahl(query: str, max_results: int = 50, start_year: int = 2020) -> List[Dict]:
    """Placeholder -- CINAHL (EBSCO) API access not yet confirmed (EBSCO
    Discovery Service API is a separate agreement from a standard EBSCO/
    CINAHL subscription)."""
    logger.warning(
        "[CINAHL] Not implemented -- no confirmed EBSCO/CINAHL API access. Use "
        "utils/manual_import.py with an exported CINAHL search instead."
    )
    return []


# ── PDF full-text download ─────────────────────────────────────────────────────

def fetch_full_text(paper_url: str) -> Optional[str]:
    """Download an arXiv PDF and extract plain text using pypdf."""
    try:
        import pypdf
    except ImportError:
        logger.warning("[PDF] pypdf not installed -- run: pip install pypdf")
        return None

    if "/abs/" in paper_url:
        arxiv_id = paper_url.split("/abs/")[-1].split("v")[0].strip()
    elif "/pdf/" in paper_url:
        arxiv_id = paper_url.split("/pdf/")[-1].replace(".pdf", "").split("v")[0].strip()
    else:
        logger.warning(f"[PDF] Cannot derive arXiv ID from URL: {paper_url}")
        return None

    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    try:
        resp = requests.get(pdf_url, headers=_HEADERS, timeout=60)
        resp.raise_for_status()
        reader = pypdf.PdfReader(io.BytesIO(resp.content))
        pages_text = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages_text).strip()
        if not text:
            logger.warning(f"[PDF] Empty text extracted from {pdf_url}")
            return None
        logger.info(f"[PDF] Extracted {len(text):,} chars from {arxiv_id} ({len(reader.pages)} pages)")
        return text[:60000]
    except Exception as exc:
        logger.warning(f"[PDF] Failed to fetch {pdf_url}: {exc}")
        return None


# ── PMC full-text fetch ────────────────────────────────────────────────────────

def fetch_pmc_fulltext(pmid: str) -> Optional[str]:
    """
    Fetch full-text XML for a PubMed article via PubMed Central (PMC).

    Steps:
      1. elink: resolve PMID -> PMC ID  (not all PubMed articles are in PMC)
      2. efetch: download the full-text XML from PMC
      3. Parse: extract plain text from <p> and <title> elements in the body

    Requires NCBI_API_KEY for 10 req/s; falls back to 3 req/s without.
    Returns None if the article is not in PMC (paywalled journals).
    """
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    key_param = {"api_key": _NCBI_API_KEY} if _NCBI_API_KEY else {}

    # ── Step 1: find the PMC ID ───────────────────────────────────────────────
    try:
        time.sleep(_NCBI_DELAY)
        r = requests.get(
            f"{base}/elink.fcgi",
            params={"dbfrom": "pubmed", "db": "pmc", "id": pmid,
                    "retmode": "json", **key_param},
            headers=_HEADERS, timeout=_TIMEOUT,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as exc:
        logger.debug(f"[PMC] elink failed for PMID {pmid}: {exc}")
        return None

    # Navigate: linksets[0] -> linksetdbs -> linkname==pubmed_pmc -> links[0]
    pmcid = None
    for ls in data.get("linksets", []):
        for lsdb in ls.get("linksetdbs", []):
            if lsdb.get("linkname") == "pubmed_pmc":
                links = lsdb.get("links", [])
                if links:
                    pmcid = str(links[0])
                    break
        if pmcid:
            break

    if not pmcid:
        logger.debug(f"[PMC] PMID {pmid} not in PMC (likely paywalled).")
        return None

    # ── Step 2: fetch the full-text XML ──────────────────────────────────────
    try:
        time.sleep(_NCBI_DELAY)
        r = requests.get(
            f"{base}/efetch.fcgi",
            params={"db": "pmc", "id": pmcid, "rettype": "full",
                    "retmode": "xml", **key_param},
            headers=_HEADERS, timeout=60,
        )
        r.raise_for_status()
        xml_text = r.text
    except Exception as exc:
        logger.warning(f"[PMC] efetch failed for PMC {pmcid}: {exc}")
        return None

    # ── Step 3: parse XML → plain text ───────────────────────────────────────
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        logger.warning(f"[PMC] XML parse error for PMC {pmcid}: {exc}")
        return None

    parts = []
    # Walk every element; collect text from meaningful tags
    for el in root.iter():
        tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag  # strip namespace
        if tag in {"title", "p", "abstract", "sec"}:
            text = (el.text or "").strip()
            if text:
                parts.append(text)
        # Also capture tail text (text after a child element closes)
        tail = (el.tail or "").strip()
        if tail:
            parts.append(tail)

    full_text = "\n".join(parts).strip()
    if not full_text:
        logger.warning(f"[PMC] Empty text parsed for PMC {pmcid}.")
        return None

    char_count = len(full_text)
    logger.info(
        f"[PMC] Full text fetched: PMID {pmid} -> PMC {pmcid} "
        f"({char_count:,} chars)"
    )
    return full_text[:60000]


# ── Deduplication ──────────────────────────────────────────────────────────────

def _deduplicate(papers: List[Dict]) -> List[Dict]:
    """Remove duplicates by normalised title."""
    seen, out = set(), []
    for p in papers:
        key = p["title"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            out.append(p)
    return out


# ── Aggregated search ──────────────────────────────────────────────────────────

def search_all(
    query: str,
    max_per_source: int = 30,
    start_year: int = 2020,
) -> Dict[str, List[Dict]]:
    """
    Query all active databases and return deduplicated results grouped by source.

    Active sources:
      - arXiv            (free, no auth)
      - Semantic Scholar (free; 1 req/s with API key)
      - CrossRef         (free, no auth)
      - OSF/SHARE        (free, no auth)
      - PubMed           (free, no auth)
    """
    logger.info(f"[DatabaseSearch] Querying all databases for: {query!r}")

    all_papers: List[Dict] = []

    # arXiv
    all_papers += search_arxiv(query, max_per_source, start_year)

    # Semantic Scholar (with API key, respects 1 req/s)
    all_papers += search_semantic_scholar(query, max_per_source, start_year)

    # CrossRef
    all_papers += search_crossref(query, max_per_source, start_year)

    # OSF / SHARE preprints
    all_papers += search_osf(query, max_per_source, start_year)

    # PubMed
    all_papers += search_pubmed(query, max_per_source, start_year)

    unique = _deduplicate(all_papers)
    logger.info(
        f"[DatabaseSearch] Total unique papers: {len(unique)} "
        f"(from {len(all_papers)} raw across all sources)"
    )

    # Group by source for the search agent's context
    by_source: Dict[str, List[Dict]] = {}
    for p in unique:
        by_source.setdefault(p["source"], []).append(p)

    return by_source


_UNPAYWALL_EMAIL = os.getenv("UNPAYWALL_EMAIL", "")


def fetch_open_access_pdf_url(doi: str) -> Optional[str]:
    """Look up a legal open-access PDF URL for a DOI via the Unpaywall API (free)."""
    if not doi or not _UNPAYWALL_EMAIL:  # Unpaywall requires a contact email (UNPAYWALL_EMAIL)
        return None
    try:
        resp = requests.get(
            f"https://api.unpaywall.org/v2/{doi}",
            params={"email": _UNPAYWALL_EMAIL},
            headers=_HEADERS,
            timeout=_TIMEOUT,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        best = data.get("best_oa_location") or {}
        return best.get("url_for_pdf") or best.get("url")
    except Exception as exc:
        logger.debug(f"[Unpaywall] Failed for DOI {doi}: {exc}")
        return None


@dataclass
class SourceSpec:
    """One entry in SOURCE_REGISTRY -- the single source of truth for "what
    database names exist, what they need, and what state they're in" that
    search_top_per_db() dispatches from. Fixes the exact problem confirmed
    live in this pipeline: a source (Web of Science, Semantic Scholar) can
    sit in ENABLED_SEARCH_DATABASES while silently contributing zero
    results, either because no connector exists yet or because of a naming
    mismatch between the configured name and the dispatcher's key. See
    search_top_per_db()'s per-source status report below, which now makes
    every one of those states explicit instead of requiring a log-grep."""
    name: str
    searcher: Optional[Callable[..., List[Dict]]]
    access_mode: str            # "api" | "manual_import" | "unavailable"
    credential_env_vars: List[str]
    availability_note: str = ""


SOURCE_REGISTRY: Dict[str, SourceSpec] = {
    "deep_research":    SourceSpec("deep_research", search_deep_research, "api", ["OPENROUTER_API_KEY"]),
    "arxiv":            SourceSpec("arxiv", search_arxiv, "api", []),
    "semantic_scholar": SourceSpec("semantic_scholar", search_semantic_scholar, "api", ["SEMANTIC_SCHOLAR_API_KEY (optional -- works without one, rate-limited)"]),
    "crossref":         SourceSpec("crossref", search_crossref, "api", []),
    "osf":              SourceSpec("osf", search_osf, "api", ["OSF_TOKEN"]),
    "pubmed":           SourceSpec("pubmed", search_pubmed, "api", ["NCBI_API_KEY (optional -- works without one, rate-limited)"]),
    "elsevier":         SourceSpec("elsevier", search_scopus, "api", ["ELSEVIER_API_KEY"]),
    "wos":              SourceSpec("wos", search_wos, "api", ["WOS_API_KEY"],
                                    "Confirmed live 2026-08-12 via Clarivate's wos-starter API. No abstracts at this tier."),
    "clinicaltrials_gov": SourceSpec("clinicaltrials_gov", search_clinicaltrials_gov, "api", [],
                                      "Free public API v2, no key. Trial-registry source, not a paper database -- see search_clinicaltrials_gov()'s docstring."),
    "central":          SourceSpec("central", search_central, "unavailable", ["COCHRANE_API_KEY (role unconfirmed for CENTRAL specifically)"],
                                    "No confirmed CENTRAL/Cochrane API access or documentation. Use manual import."),
    "embase":           SourceSpec("embase", search_embase, "unavailable", ["EMBASE_API_KEY (does not exist yet)"],
                                    "Confirmed: Embase API is a separate paid Elsevier entitlement, not covered by ELSEVIER_API_KEY. Use manual import."),
    "cinahl":           SourceSpec("cinahl", search_cinahl, "unavailable", ["EBSCO_API_KEY (does not exist yet)"],
                                    "No confirmed EBSCO/CINAHL API access. Use manual import."),
    "ictrp":            SourceSpec("ictrp", None, "unavailable", [],
                                    "No live query API found -- WHO ICTRP publishes bulk XML/CSV exports instead; needs a download+local-search adapter, not a per-query searcher. Use manual import for now."),
}


def _normalize_db_name(name: str) -> str:
    """Collapse case/underscore/hyphen/space variants so a config value like
    "SemanticScholar" (no separator) matches the registry key
    "semantic_scholar" (with one). This is the direct fix for the naming-
    mismatch bug confirmed live: ENABLED_SEARCH_DATABASES="...,
    SemanticScholar, ..." silently never matched the old hardcoded
    "semantic_scholar" dispatch key, so Semantic Scholar never ran in
    discovery despite looking enabled."""
    return re.sub(r"[\s_-]+", "", (name or "").strip().lower())


_REGISTRY_BY_NORMALIZED_NAME = {_normalize_db_name(k): k for k in SOURCE_REGISTRY}


def source_status_report(query: str = "") -> Dict[str, dict]:
    """What search_top_per_db() would do with the CURRENT
    ENABLED_SEARCH_DATABASES, without actually querying anything -- the
    "which sources are requested/available/wired" answer this design's
    §11 asks for, computable before spending a single API call."""
    enabled_raw = list(ENABLED_SEARCH_DATABASES or ("arxiv",))
    report: Dict[str, dict] = {}
    matched_keys = set()
    for raw_name in enabled_raw:
        key = _REGISTRY_BY_NORMALIZED_NAME.get(_normalize_db_name(raw_name))
        if key is None:
            report[raw_name] = {"status": "requested_but_unknown_source", "note": "not in SOURCE_REGISTRY at all"}
            continue
        matched_keys.add(key)
        spec = SOURCE_REGISTRY[key]
        if spec.searcher is None:
            report[key] = {"status": "requested_but_unimplemented", "note": spec.availability_note}
        elif spec.access_mode == "unavailable":
            report[key] = {"status": "requested_but_no_credentials", "note": spec.availability_note}
        else:
            report[key] = {"status": "requested_and_wired", "note": spec.availability_note}
    for key, spec in SOURCE_REGISTRY.items():
        if key not in matched_keys:
            report.setdefault(key, {"status": "not_requested", "note": ""})
    return report


def search_top_per_db(query: str, start_year: int = 2020, top_n: int = 50) -> Dict[str, List[Dict]]:
    """Query enabled databases and return the top-N results from each.

    Disabled database connectors stay available in this module, but the
    pipeline does not call them unless ENABLED_SEARCH_DATABASES includes them
    -- matched via _normalize_db_name() so config-value spelling variants
    (underscores, hyphens, case) can't silently fail to dispatch, the way
    "SemanticScholar" used to. Sources with no real access (access_mode
    "unavailable") or no connector at all (searcher=None, e.g. CENTRAL/
    Embase/CINAHL/ICTRP right now) are explicitly reported, not silently
    skipped -- see source_status_report(). Returns a dict keyed by enabled
    database name; value is a list of up to top_n paper dicts.

    The actual network calls (one per enabled, wired database) run
    CONCURRENTLY, not sequentially -- verified safe for this specific case
    (not a general "threads are fine" assumption): each searcher targets a
    different external host with its own independent, per-function rate-
    limit delay (no shared session object, no shared mutable state, no
    shared rate-limit counter across them -- grepped for all three before
    making this change), and each thread only ever writes to its own
    distinct `results`/`status` dict key, which is safe under the GIL
    without a lock. This does NOT generalize to fetch_fulltext_node's
    per-paper loop, where multiple papers CAN call the same rate-limited
    service (e.g. Semantic Scholar) and DO share a single output CSV --
    that one needs a real shared rate limiter and a write lock first.
    """
    enabled_raw = list(ENABLED_SEARCH_DATABASES or ("arxiv",))
    status: Dict[str, str] = {}
    to_query: List[tuple] = []  # (key, spec) pairs that actually need a network call

    # Cheap, sequential classification pass -- no I/O here, so no reason to
    # parallelize it; only the real searcher calls below go in the pool.
    for raw_name in enabled_raw:
        key = _REGISTRY_BY_NORMALIZED_NAME.get(_normalize_db_name(raw_name))
        if key is None:
            logger.warning(f"[DatabaseSearch] {raw_name!r} is not a known source (check SOURCE_REGISTRY / spelling).")
            status[raw_name] = "unknown_source"
            continue
        spec = SOURCE_REGISTRY[key]
        if spec.searcher is None:
            logger.info(f"[DatabaseSearch] {key}: requested but no connector implemented yet -- {spec.availability_note}")
            status[key] = "requested_but_unimplemented"
            continue
        if spec.access_mode == "unavailable":
            logger.info(f"[DatabaseSearch] {key}: requested but not usable -- {spec.availability_note}")
            status[key] = "requested_but_no_credentials"
            continue
        to_query.append((key, spec))

    results: Dict[str, List[Dict]] = {}

    def _run_one(key: str, spec: SourceSpec) -> List[Dict]:
        return spec.searcher(query, max_results=top_n, start_year=start_year)

    if to_query:
        with ThreadPoolExecutor(max_workers=len(to_query)) as pool:
            future_to_key = {pool.submit(_run_one, key, spec): key for key, spec in to_query}
            for future in as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    papers = future.result()
                except Exception as exc:
                    logger.warning(f"[DatabaseSearch] {key}: query failed -- {exc}")
                    status[key] = "queried_failed"
                    continue
                results[key] = papers[:top_n]
                status[key] = f"queried_ok ({len(results[key])} results)"

    found = sum(len(v) for v in results.values())
    logger.info(
        f"[DatabaseSearch] top-{top_n} per enabled DB: {found} results "
        f"across {len(results)} database(s) for: {query!r} -- status: {status}"
    )
    return results


def fetch_paper_by_title(title: str) -> Optional[Dict]:
    """
    Look up a specific paper by title on Semantic Scholar.
    Returns a paper dict (same format as search results) or None if not found.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "limit": 1,
        "fields": "paperId,title,abstract,authors,year,externalIds,openAccessPdf,url",
    }
    try:
        time.sleep(_SS_DELAY)
        r = requests.get(url, params=params, headers=_SS_HEADERS, timeout=_TIMEOUT)
        if r.status_code != 200:
            logger.warning(f"[ManualPapers] Semantic Scholar {r.status_code} for: {title[:60]}")
            return None
        data = r.json().get("data", [])
        if not data:
            logger.warning(f"[ManualPapers] No match found for: {title[:60]}")
            return None
        hit = data[0]
        authors = [a.get("name", "") for a in hit.get("authors", [])]
        ext = hit.get("externalIds", {})
        arxiv_id = ext.get("ArXiv")
        paper_url = (
            f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id
            else hit.get("url") or f"https://www.semanticscholar.org/paper/{hit['paperId']}"
        )
        # Open-access PDF: prefer arXiv PDF, then Semantic Scholar openAccessPdf
        oa = hit.get("openAccessPdf") or {}
        open_access_pdf = (
            f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id
            else oa.get("url")
        )
        return {
            "id":               f"ss:{hit['paperId']}",
            "title":            hit.get("title", title),
            "abstract":         hit.get("abstract") or "",
            "authors":          authors,
            "year":             hit.get("year") or 0,
            "url":              paper_url,
            "open_access_pdf":  open_access_pdf,
            "source":           "manual",
        }
    except Exception as exc:
        logger.warning(f"[ManualPapers] Error fetching '{title[:60]}': {exc}")
        return None
