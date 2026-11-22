"""run_service._archive_to_benchmark_runs -- after a run completes, its full
output directory is mirrored into cochrane_benchmark/runs/<label>/<model_tag>/,
matching the model-named-subfolder convention every other benchmark case
already uses. <label> is the run's external_ref (a Cochrane review id like
"CD013591", set via the dashboard's optional "Review ID" field) when one was
given, else the run_id itself. <model_tag> is whichever model
(config.MODEL_NAME) actually produced the run, read fresh at archive time.
<label>/ is also where a benchmark case's review PDF and "Included studies/"
input folder already live; this function only ever writes inside
<label>/<model_tag>/, never touching those input-side files.

One (case, model) combination = one archived run, ever: if
<label>/<model_tag>/ already holds output from a previously archived run
(detected via _ARCHIVE_MARKER_FILES), archiving is refused (logged, not
raised) rather than merging/overwriting -- re-running a case with the same
model must not silently mix a new run's files with a stale run's leftovers.

Pure archival copy: never touches the original output_dir, never raises.
"""

import json

import run_service


def _make_output_dir(tmp_path, name="session1"):
    out = tmp_path / name
    out.mkdir()
    (out / "meta_analysis_result.json").write_text(json.dumps({"pooled_g": 0.5}))
    (out / "report.md").write_text("# Report\n")
    sub = out / "subdir"
    sub.mkdir()
    (sub / "nested.txt").write_text("nested file")
    return out


class TestArchiveToBenchmarkRuns:
    def test_no_run_id_is_a_noop(self, tmp_path, monkeypatch):
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", tmp_path / "cochrane_benchmark" / "runs")
        out = _make_output_dir(tmp_path)
        run_service._archive_to_benchmark_runs(None, str(out))
        assert not (tmp_path / "cochrane_benchmark").exists()

    def test_labels_by_external_ref_when_set(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD013591"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "openai/gpt-5.6-sol")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("run123", str(out))

        dest = dest_root / "CD013591" / "gpt-5.6-sol"
        assert (dest / "meta_analysis_result.json").exists()
        assert (dest / "report.md").exists()
        assert (dest / "subdir" / "nested.txt").exists()
        assert json.loads((dest / "meta_analysis_result.json").read_text()) == {"pooled_g": 0.5}

    def test_falls_back_to_run_id_when_no_external_ref(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": None})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "openai/gpt-5.6-sol")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("run456", str(out))

        dest = dest_root / "run456" / "gpt-5.6-sol"
        assert (dest / "report.md").exists()

    def test_falls_back_to_run_id_when_run_row_missing(self, tmp_path, monkeypatch):
        """persistence disabled / row not found -- degrade to run_id, not crash."""
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run", lambda run_id: None)
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "openai/gpt-5.6-sol")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("run789", str(out))

        dest = dest_root / "run789" / "gpt-5.6-sol"
        assert (dest / "report.md").exists()

    def test_original_output_dir_untouched(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD999999"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "openai/gpt-5.6-sol")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runX", str(out))

        assert (out / "report.md").exists()  # original still there, not moved

    def test_external_ref_sanitized_for_filesystem(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD013591 / weird name"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "openai/gpt-5.6-sol")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runY", str(out))

        entries = list(dest_root.iterdir())
        assert len(entries) == 1
        assert "/" not in entries[0].name

    def test_missing_output_dir_does_not_raise(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD000000"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "openai/gpt-5.6-sol")
        run_service._archive_to_benchmark_runs("runZ", str(tmp_path / "does_not_exist"))
        assert not dest_root.exists()

    def test_get_run_raising_does_not_raise(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        def _raise(run_id):
            raise RuntimeError("db down")
        monkeypatch.setattr(run_service._run_store, "get_run", _raise)
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "openai/gpt-5.6-sol")
        out = _make_output_dir(tmp_path)
        # Must not propagate -- archiving is best-effort, never breaks a run.
        run_service._archive_to_benchmark_runs("runW", str(out))


class TestModelNamePrefix:
    """The archived subfolder name is whichever model (config.MODEL_NAME)
    actually produced the run, read fresh at archive time -- generic across
    any provider/model, never hardcoded to "claude" or "gpt" specifically.
    Lets a review directory hold runs from multiple different models side
    by side, each in its own clearly labeled subfolder."""

    def test_claude_model_produces_claude_named_folder(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD010592"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "anthropic/claude-opus-5")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runC1", str(out))

        dest = dest_root / "CD010592" / "claude-opus-5"
        assert (dest / "report.md").exists()

    def test_model_name_without_provider_slash_used_as_is(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD010592"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "some-local-model")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runC2", str(out))

        dest = dest_root / "CD010592" / "some-local-model"
        assert (dest / "report.md").exists()

    def test_model_name_with_unusual_characters_is_sanitized(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD010592"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "anthropic/claude opus:5")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runC3", str(out))

        entries = list((dest_root / "CD010592").iterdir())
        assert len(entries) == 1
        assert ":" not in entries[0].name and " " not in entries[0].name

    def test_empty_model_name_falls_back_to_unknown_model_folder(self, tmp_path, monkeypatch):
        """Never crash or produce an empty/malformed folder name if
        MODEL_NAME is unset."""
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD010592"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runC4", str(out))

        dest = dest_root / "CD010592" / "unknown_model"
        assert (dest / "report.md").exists()


class TestRefusesToOverwriteExistingRun:
    """One (case, model) combination = one archived run, ever. A case folder
    that already has input-only content (review PDF, Included studies/) but
    no pipeline output yet for THIS model is still fair game; a model
    subfolder that already has pipeline output must be left alone."""

    def test_refuses_when_marker_file_already_present(self, tmp_path, monkeypatch):
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD010592"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "google/gemini-3.8-flash")
        dest = dest_root / "CD010592" / "gemini-3.8-flash"
        dest.mkdir(parents=True)
        (dest / "paper_tracking.csv").write_text("title,year\nold study,2020\n")
        (dest / "report.md").write_text("# stale prior run\n")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runNew", str(out))

        # Refused: the stale prior run's file is untouched, the new run's
        # file was never copied in.
        assert (dest / "report.md").read_text() == "# stale prior run\n"
        assert not (dest / "meta_analysis_result.json").exists()

    def test_different_model_is_not_blocked_by_another_models_output(self, tmp_path, monkeypatch):
        """A prior GPT run's output in <CID>/gpt-5.6-sol/ must not block a
        fresh Gemini archive into <CID>/gemini-3.8-flash/."""
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD010592"})
        gpt_dest = dest_root / "CD010592" / "gpt-5.6-sol"
        gpt_dest.mkdir(parents=True)
        (gpt_dest / "paper_tracking.csv").write_text("title,year\nprior gpt run,2020\n")

        monkeypatch.setattr(run_service._config, "MODEL_NAME", "google/gemini-3.8-flash")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runGem", str(out))

        gemini_dest = dest_root / "CD010592" / "gemini-3.8-flash"
        assert (gemini_dest / "report.md").exists()
        assert (gpt_dest / "paper_tracking.csv").read_text() == "title,year\nprior gpt run,2020\n"

    def test_input_only_case_folder_is_not_treated_as_already_run(self, tmp_path, monkeypatch):
        """A benchmark case's pre-existing review PDF / Included studies/
        folder must not itself block the first archive for a given model."""
        dest_root = tmp_path / "cochrane_benchmark" / "runs"
        monkeypatch.setattr(run_service, "BENCHMARK_RUNS_DIR", dest_root)
        monkeypatch.setattr(run_service._run_store, "get_run",
                             lambda run_id: {"external_ref": "CD010592"})
        monkeypatch.setattr(run_service._config, "MODEL_NAME", "google/gemini-3.8-flash")
        case_dir = dest_root / "CD010592"
        (case_dir / "Included studies").mkdir(parents=True)
        (case_dir / "CD010592.pdf").write_text("not a real pdf, just a placeholder")
        out = _make_output_dir(tmp_path)

        run_service._archive_to_benchmark_runs("runFirst", str(out))

        dest = case_dir / "gemini-3.8-flash"
        assert (dest / "report.md").exists()
        assert (case_dir / "CD010592.pdf").exists()  # untouched input-side file
        assert (case_dir / "Included studies").is_dir()  # untouched input-side folder
