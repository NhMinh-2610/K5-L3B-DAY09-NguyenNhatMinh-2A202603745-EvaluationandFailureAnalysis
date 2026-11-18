"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence
from math import comb, isfinite
from numbers import Integral

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    if len(human) != len(judge):
        raise ValueError("human and judge must have the same number of labels")
    counts = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for actual, predicted in zip(human, judge):
        if actual not in ("PASS", POS) or predicted not in ("PASS", POS):
            raise ValueError("labels must be PASS or FAIL")
        if actual == POS:
            counts["tp" if predicted == POS else "fn"] += 1
        else:
            counts["fp" if predicted == POS else "tn"] += 1
    return counts


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    counts = confusion(human, judge)
    predicted_failures = counts["tp"] + counts["fp"]
    actual_failures = counts["tp"] + counts["fn"]
    precision = counts["tp"] / predicted_failures if predicted_failures else 0.0
    recall = counts["tp"] / actual_failures if actual_failures else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    counts = confusion(human, judge)
    n = sum(counts.values())
    if n == 0:
        raise ValueError("kappa is undefined for empty labels")
    observed_agreement = (counts["tp"] + counts["tn"]) / n
    human_fail_rate = (counts["tp"] + counts["fn"]) / n
    judge_fail_rate = (counts["tp"] + counts["fp"]) / n
    expected_agreement = (human_fail_rate * judge_fail_rate
                          + (1 - human_fail_rate) * (1 - judge_fail_rate))
    if expected_agreement == 1.0:
        raise ValueError("kappa is undefined when expected agreement is 1")
    return (observed_agreement - expected_agreement) / (1 - expected_agreement)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    for name, value in (("observed_rate", observed_rate), ("sensitivity", sensitivity),
                        ("specificity", specificity)):
        if not isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"{name} must be a finite probability in [0, 1]")
    denominator = sensitivity + specificity - 1
    if denominator == 0:
        raise ValueError("Rogan-Gladen is undefined when sensitivity + specificity is 1")
    corrected = (observed_rate + specificity - 1) / denominator
    return min(1.0, max(0.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy.stats import bootstrap

    pr = np.asarray(a, dtype=float)
    baseline = np.asarray(b, dtype=float)
    if pr.ndim != 1 or baseline.ndim != 1 or len(pr) != len(baseline) or len(pr) == 0:
        raise ValueError("paired bootstrap requires non-empty 1D arrays of the same length")
    if not np.isfinite(pr).all() or not np.isfinite(baseline).all():
        raise ValueError("paired bootstrap requires finite values")
    if isinstance(n_resamples, bool) or not isinstance(n_resamples, Integral) or n_resamples <= 0:
        raise ValueError("n_resamples must be a positive integer")
    if not isfinite(confidence) or not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    if np.array_equal(pr, baseline):
        return 0.0, 0.0, 0.0
    if len(pr) < 2:
        raise ValueError("a confidence interval requires at least two paired items")

    def mean_difference(x, y, axis=-1):
        return np.mean(x, axis=axis) - np.mean(y, axis=axis)

    result = bootstrap((pr, baseline), mean_difference, paired=True,
                       n_resamples=int(n_resamples), method="percentile",
                       confidence_level=confidence, rng=np.random.default_rng(rng))
    delta = float(np.mean(pr) - np.mean(baseline))
    return delta, float(result.confidence_interval.low), float(result.confidence_interval.high)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    n, c, k = _trial_counts(n, c, k)
    return 1.0 if n - c < k else 1.0 - comb(n - c, k) / comb(n, k)


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    n, c, k = _trial_counts(n, c, k)
    return 0.0 if c < k else comb(c, k) / comb(n, k)


def _trial_counts(n: int, c: int, k: int) -> tuple[int, int, int]:
    if any(isinstance(value, bool) or not isinstance(value, Integral) for value in (n, c, k)):
        raise ValueError("n, c and k must be integer counts")
    if n < 1 or not 0 <= c <= n or not 1 <= k <= n:
        raise ValueError("require n >= 1, 0 <= c <= n and 1 <= k <= n")
    return int(n), int(c), int(k)
