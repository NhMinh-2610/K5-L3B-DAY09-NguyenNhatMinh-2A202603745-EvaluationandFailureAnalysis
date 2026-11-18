"""Regression evidence for FM-03 on the public C-002 case."""

import pytest

from pydantic_evals.evaluators import EvaluatorContext

from lab9.graders import DbFactKept
from lab9.trace_case import investigate


pytestmark = pytest.mark.student


def grade_db_fact(case):
    trial = case["trial"]
    result = trial["result"]
    ctx = EvaluatorContext(
        name=result["run_id"],
        inputs={"claim_id": result["claim_id"], "seed": result["seed"]},
        metadata=None,
        expected_output=case["label"],
        output=trial,
        duration=0.0,
        _span_tree=None,
        attributes={},
        metrics={},
    )
    return DbFactKept().evaluate(ctx)


@pytest.mark.parametrize("shape,seed", [("seeded_regression", 11), ("swarm", 55)])
def test_lab9_trace_case_detects_ticket_override(shape, seed):
    case = investigate(shape, "C-002", seed)
    assert grade_db_fact(case).value is False
    assert case["trial"]["lab8_pass"] is False
    assert case["trial"]["result"]["status"] == "resolved"
    assert case["trial"]["snapshot"]["refund_vnd"] == 20000
    assert case["label"]["refund_vnd"] == 0


@pytest.mark.parametrize("seed", [11, 55])
def test_lab9_trace_case_fixed_keeps_db_fact(seed):
    case = investigate("fixed", "C-002", seed)
    assert grade_db_fact(case).value is True
    assert case["trial"]["lab8_pass"] is True
    assert case["trial"]["result"]["status"] == "denied"
    assert case["trial"]["snapshot"]["refund_vnd"] == 0


def test_lab9_trace_case_reference_control_on_non_override_seed():
    case = investigate("swarm", "C-002", 11)
    assert grade_db_fact(case).value is True
    assert case["trial"]["lab8_pass"] is True
    assert case["trial"]["result"]["status"] == "denied"
    assert case["trial"]["snapshot"]["refund_vnd"] == 0
