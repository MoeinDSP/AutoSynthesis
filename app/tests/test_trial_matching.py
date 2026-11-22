"""utils/trial_matching.py -- distinguishing a study/trial from the
individual publication(s) that report it. Conservative by design: only
registry-ID and DOI exact matches count as a same-trial match (see module
docstring for why fuzzy title/author heuristics are deliberately excluded)."""

from models import PaperRecord
from utils.trial_matching import extract_registry_ids, match_same_trial, assign_trial_clusters


def _paper(id_, **kwargs):
    defaults = dict(title=f"Paper {id_}", abstract="", year=2020, source="manual")
    defaults.update(kwargs)
    return PaperRecord(id=id_, **defaults)


def test_extract_registry_ids_finds_nct_and_normalizes_case():
    ids = extract_registry_ids("This trial was registered as NCT01234567 on ClinicalTrials.gov.")
    assert ids == ["NCT01234567"]


def test_extract_registry_ids_finds_multiple_formats():
    text = "Registered as ISRCTN12345678 and cross-referenced with EUCTR2008-002159-25-FR."
    ids = extract_registry_ids(text)
    assert "ISRCTN12345678" in ids
    assert "EUCTR2008-002159-25-FR" in ids


def test_extract_registry_ids_empty_for_no_match():
    assert extract_registry_ids("No registry mentioned here.") == []
    assert extract_registry_ids(None) == []


def test_same_registry_id_in_full_text_matches_two_papers():
    a = _paper("a", full_text="This RCT (NCT01234567) enrolled 200 patients...")
    b = _paper("b", title="A completely different title",
               full_text="Secondary analysis of trial NCT01234567 assessing quality of life...")
    is_same, reason, confidence = match_same_trial(a, b)
    assert is_same is True
    assert "trial_registry_id" in reason
    assert confidence == 1.0


def test_same_doi_matches():
    a = _paper("a", doi="10.1000/xyz123")
    b = _paper("b", doi="https://doi.org/10.1000/XYZ123")
    is_same, reason, _ = match_same_trial(a, b)
    assert is_same is True
    assert reason == "doi_exact"


def test_different_papers_no_shared_evidence_not_matched():
    a = _paper("a", full_text="A trial of drug X in condition Y (NCT01111111).")
    b = _paper("b", full_text="An unrelated trial of drug Z in condition W (NCT02222222).")
    is_same, reason, confidence = match_same_trial(a, b)
    assert is_same is False
    assert reason == "none"
    assert confidence == 0.0


def test_similar_titles_alone_do_not_match_conservative_by_design():
    # Title similarity is deliberately NOT a matching signal here (unlike
    # cochrane_benchmark's GT-vs-candidate matcher) -- two genuinely
    # different papers on a similar topic must never be merged just because
    # they read alike.
    a = _paper("a", title="Effect of drug X on outcome Y: a randomized trial")
    b = _paper("b", title="Effect of drug X on outcome Y: a randomized study")
    is_same, reason, _ = match_same_trial(a, b)
    assert is_same is False


def test_assign_trial_clusters_groups_companion_papers():
    papers = [
        _paper("a", full_text="Trial NCT01234567 primary outcome paper..."),
        _paper("b", full_text="Trial NCT01234567 secondary analysis paper..."),
        _paper("c", full_text="Unrelated trial NCT09999999..."),
    ]
    assign_trial_clusters(papers)
    a, b, c = papers
    assert a.trial_cluster_id is not None
    assert a.trial_cluster_id == b.trial_cluster_id
    assert c.trial_cluster_id is None  # no companion found -- unaffected


def test_assign_trial_clusters_stable_id_not_name_derived():
    papers = [
        _paper("study_x", full_text="NCT01234567 report A"),
        _paper("study_y", full_text="NCT01234567 report B"),
    ]
    assign_trial_clusters(papers)
    cluster_id = papers[0].trial_cluster_id
    assert cluster_id is not None
    assert "study_x" not in cluster_id and "study_y" not in cluster_id
    assert cluster_id.startswith("trial_")


def test_assign_trial_clusters_three_way_transitivity():
    # a<->b via registry id, b<->c via a shared DOI -- all three must end up
    # in ONE cluster (union-find transitivity), not two separate pairs.
    papers = [
        _paper("a", full_text="NCT01234567 paper A", doi=None),
        _paper("b", full_text="NCT01234567 paper B", doi="10.1/shared"),
        _paper("c", full_text="no registry mentioned here", doi="10.1/shared"),
    ]
    assign_trial_clusters(papers)
    ids = {p.trial_cluster_id for p in papers}
    assert len(ids) == 1
    assert None not in ids
