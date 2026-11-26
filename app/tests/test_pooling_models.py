"""Pooling models (fixed effect, every metafor random-effects estimator, UWLS) and the
publication-bias tests (Egger, Begg, trim-and-fill, PET-PEESE). UWLS and PET-PEESE are
checked against an independent numpy implementation of weighted least squares."""
import math

import numpy as np
import pytest

pytest.importorskip("rpy2")
from statistics import metafor_engine as m                      # noqa: E402
from statistics.heterogeneity import compute_all               # noqa: E402
from statistics.publication_bias import pet_peese, rank_test, trim_and_fill, eggers_test  # noqa: E402
from scipy import stats                                         # noqa: E402

Y = [0.10, 0.30, 0.35, 0.65, 0.45, 0.15, 0.80, 0.52, 0.20, 0.41, 0.60]
V = [0.03, 0.02, 0.05, 0.01, 0.04, 0.02, 0.09, 0.03, 0.015, 0.02, 0.07]


def _wls(x=None):
    y, v = np.array(Y), np.array(V)
    w = 1 / v
    X = np.ones((len(y), 1)) if x is None else np.column_stack([np.ones(len(y)), x])
    xtwx = X.T @ (w[:, None] * X)
    beta = np.linalg.solve(xtwx, X.T @ (w * y))
    s2 = (w * (y - X @ beta) ** 2).sum() / (len(y) - X.shape[1])
    se = math.sqrt((s2 * np.linalg.inv(xtwx))[0, 0])
    return beta[0], se, len(y) - X.shape[1]


@pytest.mark.parametrize("method", list(m.POOLING_MODELS))
def test_every_model_pools(method):
    r = m.pool(Y, V, method=method)
    assert r["method"] == method
    assert r["ci_lower"] < r["pooled_g"] < r["ci_upper"]
    assert abs(sum(r["weights"]) - 100) < 1e-6


def test_fe_has_no_tau2_and_matches_inverse_variance():
    w = 1 / np.array(V)
    r = m.pool(Y, V, method="FE")
    assert r["tau_squared"] == 0
    assert r["pooled_g"] == pytest.approx((w * np.array(Y)).sum() / w.sum(), abs=1e-10)


def test_uwls_matches_weighted_least_squares():
    est, se, df = _wls()
    r = m.pool(Y, V, method="UWLS")
    t = stats.t.ppf(0.975, df)
    assert r["pooled_g"] == pytest.approx(est, abs=1e-10)
    assert r["pooled_se"] == pytest.approx(se, abs=1e-10)
    assert r["ci_lower"] == pytest.approx(est - t * se, abs=1e-8)
    # UWLS has the fixed-effect point estimate
    assert r["pooled_g"] == pytest.approx(m.pool(Y, V, method="FE")["pooled_g"], abs=1e-10)


def test_uwls_on_ratio_scale_back_transforms():
    r = m.pool_log_measure([math.log(0.8), math.log(0.9), math.log(0.7)], [0.04, 0.05, 0.03], method="UWLS")
    assert r["pooled_ratio"] == pytest.approx(math.exp(r["pooled_g"]))


def test_unknown_model_falls_back_to_reml():
    assert m.normalize_pooling_model("nonsense") == "REML"
    assert m.normalize_pooling_model(None) == "REML"
    assert m.normalize_pooling_model("fixed") == "FE"


def test_heterogeneity_follows_random_effects_estimator_and_uses_reml_for_fe_uwls():
    assert compute_all(Y, V, method="DL")["tau_squared"] == pytest.approx(m.pool(Y, V, method="DL")["tau_squared"], abs=1e-6)
    assert compute_all(Y, V, method="UWLS") == compute_all(Y, V, method="REML")


def test_pet_peese_match_weighted_least_squares():
    pp = pet_peese(Y, V)
    pet_est, pet_se, _ = _wls(np.sqrt(V))
    peese_est, peese_se, _ = _wls(np.array(V))
    assert pp["pet"]["estimate"] == pytest.approx(pet_est, abs=1e-4)
    assert pp["pet"]["se"] == pytest.approx(pet_se, abs=1e-4)
    assert pp["peese"]["estimate"] == pytest.approx(peese_est, abs=1e-4)
    # conditional rule: PET intercept significant -> PEESE, else PET
    expected = "PEESE" if pp["pet"]["p_value"] < 0.05 else "PET"
    assert pp["selected"] == expected


def test_pet_peese_flags_small_k_and_skips_tiny_k():
    assert "unreliable" in pet_peese(Y[:5], V[:5])["note"]
    assert "Too few" in pet_peese(Y[:2], V[:2])["note"]


def test_egger_intercept_under_fe_equals_pet():
    # metafor's regtest limit estimate with a fixed-effect fit is the PET intercept
    assert eggers_test(Y, V, method="FE")["intercept"] == pytest.approx(pet_peese(Y, V)["pet"]["estimate"], abs=1e-4)


def test_rank_test_and_trim_and_fill_run():
    rt = rank_test(Y, V)
    assert -1 <= rt["kendall_tau"] <= 1 and 0 <= rt["p_value"] <= 1
    tf = trim_and_fill(Y, V, side=None, method="UWLS")
    assert tf["side"] in ("left", "right") and tf["k0"] >= 0
