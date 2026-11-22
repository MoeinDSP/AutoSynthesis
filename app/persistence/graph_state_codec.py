"""JSON-safe round-trip for `pipeline_graph.GraphState` dicts.

Most of GraphState's ~40 keys are already JSON-native (strings, ints,
lists-of-dicts, etc.) -- only a handful carry actual Pydantic model
instances, which `json.dumps`/`jsonb` can't serialize directly. This module
is the single explicit map of which keys need model-aware handling.

Correctness-critical subset: at the two pause boundaries this pipeline
actually persists mid-run (see run_pause_states in the schema), only `plan`,
`papers_eligible`, and `all_retrieved_papers` are populated -- nothing
downstream of eligibility_node has run yet. Those three round-tripping
perfectly is what matters most; the rest only matter for the terminal
snapshot, where a codec bug can't corrupt an in-flight run.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Type

from pydantic import BaseModel

from models import (
    MetaAnalysisPlan, PaperRecord, EffectSizeRecord, MetaAnalysisResult,
    MetaAnalysisGroupResult, ModeratorResult, BiasResult, RiskOfBiasAssessment,
    ValidationFlag,
)

# key -> the ONE model class held there (a bare instance, not a list)
_SINGLE_MODEL_KEYS: Dict[str, Type[BaseModel]] = {
    "plan": MetaAnalysisPlan,
    "meta_result": MetaAnalysisResult,
    "bias_result": BiasResult,
}

# key -> the model class each element of the list is
_LIST_MODEL_KEYS: Dict[str, Type[BaseModel]] = {
    "papers_eligible": PaperRecord,
    "all_retrieved_papers": PaperRecord,
    "effect_sizes": EffectSizeRecord,
    "meta_results": MetaAnalysisGroupResult,
    "moderator_results": ModeratorResult,
    "rob_assessments": RiskOfBiasAssessment,
    "validation_flags": ValidationFlag,
}


def dump_graph_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """GraphState dict -> plain, JSON-safe dict (jsonb-storable). Unknown
    keys pass through unchanged (already JSON-native). If dumping still
    leaves something non-JSON-serializable (a Pydantic instance under a key
    this module doesn't know about), raises loudly rather than silently
    storing something `load_graph_state` couldn't reconstruct -- that's a
    codec bug that needs fixing, not swallowing."""
    out: Dict[str, Any] = {}
    for key, value in state.items():
        if value is None:
            out[key] = None
        elif key in _SINGLE_MODEL_KEYS:
            out[key] = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
        elif key in _LIST_MODEL_KEYS:
            out[key] = [
                item.model_dump(mode="json") if isinstance(item, BaseModel) else item
                for item in value
            ]
        else:
            out[key] = value

    # Safety net: if anything is still a bare Pydantic instance (a new
    # model-holding key added to GraphState without updating this codec),
    # json.dumps will raise TypeError -- catch it and name the offending
    # key explicitly instead of letting an opaque serialization error
    # surface deep inside a DB write.
    try:
        json.dumps(out, default=_reject_unknown)
    except TypeError as exc:
        raise TypeError(
            f"graph_state_codec.dump_graph_state: encountered a value it doesn't know how "
            f"to serialize ({exc}). If GraphState gained a new key holding a Pydantic model "
            f"or other non-JSON-native type, add it to _SINGLE_MODEL_KEYS/_LIST_MODEL_KEYS "
            f"in this file."
        ) from exc
    return out


def _reject_unknown(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        raise TypeError(f"unhandled Pydantic instance of type {type(obj).__name__}")
    raise TypeError(f"unhandled type {type(obj).__name__}")


def load_graph_state(data: Dict[str, Any]) -> Dict[str, Any]:
    """Plain dict (as stored in jsonb, or round-tripped through json) ->
    GraphState dict with the correct Pydantic instances reconstructed under
    the keys in _SINGLE_MODEL_KEYS/_LIST_MODEL_KEYS. Inverse of
    dump_graph_state -- for any state produced by dump_graph_state, the
    round trip is a deep-equality no-op."""
    out: Dict[str, Any] = {}
    for key, value in data.items():
        if value is None:
            out[key] = None
        elif key in _SINGLE_MODEL_KEYS:
            out[key] = _SINGLE_MODEL_KEYS[key](**value)
        elif key in _LIST_MODEL_KEYS:
            cls = _LIST_MODEL_KEYS[key]
            out[key] = [cls(**item) for item in value]
        else:
            out[key] = value
    return out
