def test_deterministic_row_signal_finds_core_numbers_and_quote():
    from agents.statistical_result_checker_agent import _deterministic_row_signal

    text = (
        "The mindfulness group improved more than control, t(58) = 2.31, "
        "p = .03. The mindfulness mean was 4.20 with SD = 1.10."
    )
    row = {
        "test_statistic": 2.31,
        "p_value": 0.03,
        "group_1_mean": 4.2,
        "group_1_sd": 1.1,
        "evidence_quote": "mindfulness group improved more than control, t(58) = 2.31",
    }

    signal = _deterministic_row_signal(row, text)

    assert signal["strong_match"] is True
    assert "test_statistic" in signal["verified_stats"]
    assert "p_value" in signal["verified_stats"]
    assert signal["evidence_quote_found"] is True
