"""M4 checks for pairing, PR-minus-baseline direction and invalid observations."""

import pytest

from lab9.stats import paired_bootstrap


pytestmark = pytest.mark.student


def test_lab9_bootstrap_keeps_shared_item_variation_paired():
    # Large differences between items must not create uncertainty about an
    # improvement that is exactly one unit for every matched item.
    assert paired_bootstrap([101, 201, 301, 401], [100, 200, 300, 400]) == (1.0, 1.0, 1.0)


def test_lab9_bootstrap_reverses_ci_when_pr_and_baseline_are_swapped():
    a, b = [1.0, 0.5, 1.0, 0.0], [0.7, 0.3, 0.4, 0.0]
    delta, low, high = paired_bootstrap(a, b)
    reversed_delta, reversed_low, reversed_high = paired_bootstrap(b, a)
    assert reversed_delta == pytest.approx(-delta)
    assert reversed_low == pytest.approx(-high)
    assert reversed_high == pytest.approx(-low)


@pytest.mark.parametrize("a,b", [([], []), ([1, 0], [1]), ([1], [0]),
                                 ([1, float("nan")], [1, 0]),
                                 ([1, 0], [1, float("inf")])])
def test_lab9_bootstrap_rejects_unusable_pairs(a, b):
    with pytest.raises(ValueError):
        paired_bootstrap(a, b)
