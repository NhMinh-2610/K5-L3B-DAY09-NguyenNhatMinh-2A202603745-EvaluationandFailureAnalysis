"""Adversarial report checks and slice tests independent of variant names."""

import copy
import math

import pytest

from lab9 import gate, stats


pytestmark = pytest.mark.student


def example():
    seeds = [11, 22, 33, 44, 55]
    rows = [{"item_id": f"E-{i:03d}", "seed": seed, "pass_rate": True,
             "secret_leak": False, "cost": 1.0,
             "slices": ["money_movement"] if i < 2 else ["adversarial"]}
            for i in range(4) for seed in seeds]
    report = {"manifest": {"eval_set_sha": "fixture", "items": 4, "seeds": seeds,
                           "metric_spec_version": "2.0"},
              "rows": rows, "evaluator_failures": [],
              "metrics": {"pass_rate": 1.0, "secret_leak": 0, "cost_per_success": 1.0}}
    spec = {"eval_set_version": "v2", "metric_spec_version": "2.0", "seeds": seeds,
            "metrics": [
                {"id": "pass_rate", "kind": "capability", "blocking": True,
                 "threshold": {"min": 0.8, "no_significant_drop": True}},
                {"id": "secret_leak", "kind": "safety", "blocking": True, "threshold": {"max": 0}},
                {"id": "cost_per_success", "kind": "system", "blocking": False,
                 "threshold": {"max_increase": 0.1}}],
            "slices": [{"name": "money_movement", "metric": "pass_rate", "min": 0.9,
                        "no_significant_drop": True, "blocking": True}]}
    return report, spec


def test_lab9_advanced_identical_valid_report_merges():
    report, spec = example()
    assert gate.check(copy.deepcopy(report), report, spec, copy.deepcopy(spec))[0] == []


def test_lab9_advanced_duplicate_replacing_another_row_is_not_a_complete_grid():
    base, spec = example()
    pr = copy.deepcopy(base)
    pr["rows"][0] = copy.deepcopy(pr["rows"][1])
    problems = gate.integrity_check(pr, base, spec)
    assert any("duplicate" in p for p in problems)


def test_lab9_advanced_evaluator_failure_on_green_report_blocks():
    base, spec = example()
    pr = copy.deepcopy(base)
    pr["evaluator_failures"] = ["E-000@11:grader failed"]
    assert gate.check(pr, base, spec)[0] == ["integrity"]


def test_lab9_advanced_relabelling_a_slice_blocks():
    base, spec = example()
    pr = copy.deepcopy(base)
    for row in pr["rows"]:
        if row["item_id"] == "E-000":
            row["slices"] = []
    assert gate.integrity_check(pr, base, spec)


def test_lab9_advanced_edited_summary_is_recomputed_from_rows():
    base, spec = example()
    pr = copy.deepcopy(base)
    pr["metrics"]["pass_rate"] = 0.99
    assert any("summary pass_rate" in p for p in gate.integrity_check(pr, base, spec))


def test_lab9_advanced_missing_grade_cannot_fall_out_of_the_mean():
    base, spec = example()
    pr = copy.deepcopy(base)
    pr["rows"][0]["pass_rate"] = None
    assert gate.integrity_check(pr, base, spec)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_lab9_advanced_nonfinite_values_block(value):
    base, spec = example()
    pr = copy.deepcopy(base)
    pr["metrics"]["pass_rate"] = value
    assert gate.check(pr, base, spec)[0] == ["integrity"]


@pytest.mark.parametrize("change", ["drop_metric", "unblock", "lower_min", "raise_max",
                                     "raise_cost", "drop_ci", "drop_slice", "unblock_slice",
                                     "lower_slice", "drop_slice_ci", "bump_version_and_loosen"])
def test_lab9_advanced_ratchet_rejects_policy_weakening(change):
    base, original = example()
    pr, spec = copy.deepcopy(base), copy.deepcopy(original)
    if change == "drop_metric":
        spec["metrics"].pop()
    elif change == "unblock":
        spec["metrics"][0]["blocking"] = False
    elif change in ("lower_min", "bump_version_and_loosen"):
        spec["metrics"][0]["threshold"]["min"] = 0.7
        if change == "bump_version_and_loosen":
            spec["metric_spec_version"] = pr["manifest"]["metric_spec_version"] = "2.1"
    elif change == "raise_max":
        spec["metrics"][1]["threshold"]["max"] = 1
    elif change == "raise_cost":
        spec["metrics"][2]["threshold"]["max_increase"] = 0.2
    elif change == "drop_ci":
        spec["metrics"][0]["threshold"].pop("no_significant_drop")
    elif change == "drop_slice":
        spec["slices"] = []
    elif change == "unblock_slice":
        spec["slices"][0]["blocking"] = False
    elif change == "lower_slice":
        spec["slices"][0]["min"] = 0.8
    else:
        spec["slices"][0].pop("no_significant_drop")
    assert any("ratchet" in p for p in gate.integrity_check(pr, base, spec, original))


def test_lab9_advanced_ratchet_accepts_stricter_policy_and_new_spec_version():
    base, old = example()
    pr, spec = copy.deepcopy(base), copy.deepcopy(old)
    spec["metric_spec_version"] = pr["manifest"]["metric_spec_version"] = "2.1"
    spec["metrics"][0]["threshold"]["min"] = 0.9
    spec["slices"][0]["min"] = 0.95
    assert gate.check(pr, base, spec, old)[0] == []


@pytest.mark.parametrize("slice_name", ["money_movement", "unseen_priority"])
def test_lab9_advanced_slice_ci_catches_drop_above_absolute_floor(slice_name):
    base, spec = example()
    for row in base["rows"]:
        if row["item_id"] in {"E-000", "E-001"}:
            row["slices"] = [slice_name]
    spec["slices"][0].update(name=slice_name, min=0.5)
    pr = copy.deepcopy(base)
    for row in pr["rows"]:
        if slice_name in row["slices"] and row["seed"] == 11:
            row["pass_rate"] = False
    pr["metrics"]["pass_rate"] = 0.9
    pr["metrics"]["cost_per_success"] = round(20 / 18, 4)
    blocked, _ = gate.check(pr, base, spec)
    assert blocked == [f"slice:{slice_name}/pass_rate"]


@pytest.mark.parametrize("args", [(0, 0, 1), (5, -1, 1), (5, 6, 1), (5, 2, 0),
                                   (5, 2, 6), (5.0, 2, 1), (5, True, 1)])
def test_lab9_advanced_pass_estimators_validate_all_counts(args):
    for fn in (stats.pass_at_k, stats.pass_hat_k):
        with pytest.raises(ValueError):
            fn(*args)


def test_lab9_advanced_pass_estimators_obey_bounds_and_complement_identity():
    for n in range(1, 13):
        for c in range(n + 1):
            for k in range(1, n + 1):
                at, all_pass = stats.pass_at_k(n, c, k), stats.pass_hat_k(n, c, k)
                assert -1e-12 <= all_pass <= c / n + 1e-12 <= at + 2e-12 <= 1 + 3e-12
                assert math.isclose(at + stats.pass_hat_k(n, n - c, k), 1, abs_tol=1e-12)
