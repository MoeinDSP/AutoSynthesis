"""
Verifies the graph compiles without error and all nodes are importable.
Does not make any LLM API calls.
"""


def test_compiled_graph_is_importable():
    from pipeline_graph import compiled_graph
    assert compiled_graph is not None


def test_graph_has_all_nodes():
    from pipeline_graph import compiled_graph
    node_names = set(compiled_graph.get_graph().nodes.keys())
    required = {
        "plan_node", "manual_ingest_node", "document_type_node",
        "search_node", "fetch_fulltext_node",
        "eligibility_node", "paper_tracking_review_node",
        "study_detection_node", "extraction_node",
        "validation_node", "relevance_filter_node", "mapping_node",
        "export_table_node", "effect_size_node", "meta_analysis_node",
        "moderator_node", "bias_node", "risk_of_bias_node", "report_node",
    }
    missing = required - node_names
    assert not missing, f"Missing nodes: {missing}"


def test_all_agent_nodes_importable():
    from agents.planning_agent              import plan_node
    from agents.search_agent               import search_node
    from agents.eligibility_agent          import eligibility_node
    from agents.paper_reading_agent        import (manual_ingest_node,
                                                    fetch_fulltext_node)
    from agents.document_type_agent        import document_type_node
    from agents.study_detector_agent       import study_detection_node
    from agents.statistical_result_extractor_agent import extraction_node
    from agents.statistical_result_checker_agent   import validation_node
    from agents.relevance_filter_agent     import relevance_filter_node
    from agents.cross_paper_outcome_mapper_agent   import mapping_node
    from agents.effect_size_agent          import effect_size_node, export_table_node
    from agents.meta_analysis_agent        import meta_analysis_node
    from agents.moderator_agent            import moderator_node
    from agents.bias_agent                 import bias_node
    from agents.risk_of_bias_agent         import risk_of_bias_node
    from agents.report_agent               import report_node
    assert True


def test_orchestrator_adapter_importable():
    from orchestrator import MetaAnalysisOrchestrator
    orch = MetaAnalysisOrchestrator(output_dir="/tmp/test_meta")
    assert hasattr(orch, "run")
    assert hasattr(orch, "run_until_review")
    assert hasattr(orch, "continue_after_review")
    assert hasattr(orch, "run_downstream")
