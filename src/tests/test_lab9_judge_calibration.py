"""M2 edge cases and replay calibration decisions, without running a model."""

from pathlib import Path

import pytest

from lab9 import stats
from lab9.judge import calibrate


pytestmark = pytest.mark.student


@pytest.mark.parametrize("human,judge", [([], []), (["FAIL", "PASS"], ["PASS", "PASS"]),
                                         (["PASS"], ["FAIL"])])
def test_lab9_precision_recall_zero_denominators(human, judge):
    assert stats.precision_recall(human, judge) == (0.0, 0.0)


def test_lab9_confusion_rejects_unpaired_or_invalid_labels():
    with pytest.raises(ValueError):
        stats.confusion(["FAIL", "PASS"], ["FAIL"])
    with pytest.raises(ValueError):
        stats.confusion(["PASS"], ["UNKNOWN"])


@pytest.mark.parametrize("judge,want", [(["PASS", "FAIL"], 1.0),
                                       (["FAIL", "PASS"], -1.0),
                                       (["PASS", "PASS"], 0.0)])
def test_lab9_kappa_perfect_opposite_and_constant_predictions(judge, want):
    assert stats.cohen_kappa(["PASS", "FAIL"], judge) == pytest.approx(want)


def test_lab9_kappa_rejects_empty_labels():
    with pytest.raises(ValueError):
        stats.cohen_kappa([], [])


def test_lab9_rogan_gladen_recovers_prevalence_and_clips_upper_bound():
    assert stats.rogan_gladen(0.24, 0.8, 0.9) == pytest.approx(0.2)
    assert stats.rogan_gladen(1.0, 0.8, 0.9) == 1.0


@pytest.mark.parametrize("args", [(0.5, 0.5, 0.5), (float("nan"), 0.8, 0.9),
                                  (0.2, 1.1, 0.9), (0.2, 0.8, -0.1)])
def test_lab9_rogan_gladen_rejects_undefined_or_invalid_inputs(args):
    with pytest.raises(ValueError):
        stats.rogan_gladen(*args)


def test_lab9_replayed_judges_meet_expected_calibration_decisions():
    tone = calibrate(Path("data/eval/judge_tone_public.csv"))
    helpful = calibrate(Path("data/eval/judge_helpful_public.csv"))
    assert tone["passed"] is True
    assert helpful["passed"] is False
    assert helpful["confusion"] == {"tp": 9, "fp": 0, "fn": 21, "tn": 70}
    assert helpful["recall"] < 0.7 and helpful["kappa"] < 0.6
