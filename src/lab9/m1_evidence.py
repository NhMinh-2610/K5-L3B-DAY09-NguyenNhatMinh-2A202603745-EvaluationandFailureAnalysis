"""Replay public cases for the M1 taxonomy without changing Lab 8 or the variants.

Run from src/: python -m lab9.m1_evidence
The m1_* shapes only select existing bug switches in memory. This script records
raw trials and fixed controls; it does not implement or replace a grader.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lab8.console import utf8_stdio
from lab8.shapes import SHAPES
from lab9.evalset import SOURCE, load_jsonl, sha12
from lab9.trace_case import investigate
from lab9.variant_agent import make_shape


# One bug at a time makes the first wrong step easier to identify. The real swarm
# and seeded_regression are also replayed, using the same public claim and seed.
CASES = (
    ("FM-01", "m1_leaky_trace", "C-010", 11, ("no_override", "leaky_trace")),
    ("FM-02", "m1_ignore_denied", "C-007", 11, ("no_override", "ignore_denied")),
    ("FM-03", "seeded_regression", "C-002", 11, ()),
    ("FM-03", "swarm", "C-002", 55, ()),
    ("FM-04", "m1_sum_parts", "C-014", 11, ("no_override", "sum_parts")),
    ("FM-04", "m1_round_down", "C-001", 11, ("no_override", "round_down")),
    ("FM-05", "m1_pre_deducted", "C-014", 11, ("no_override", "pre_deducted")),
    ("FM-05", "seeded_regression", "C-013", 11, ()),
    ("FM-02", "m1_ignore_denied", "C-013", 11, ("no_override", "ignore_denied")),
    ("FM-06", "m1_stale_clause", "C-006", 11, ("no_override", "stale_clause")),
    ("FM-07", "m1_sibling_refund", "C-001", 11, ("no_override", "sibling_refund")),
    ("FM-08", "m1_misreport", "C-008", 11, ("no_override", "misreport")),
)


def collect() -> dict:
    controls: dict[tuple[str, int], dict] = {}
    cases = []
    for mode, shape, claim_id, seed, bugs in CASES:
        if bugs:
            SHAPES[shape] = make_shape(shape, frozenset(bugs))
        case = investigate(shape, claim_id, seed)
        key = (claim_id, seed)
        if key not in controls:
            controls[key] = investigate("fixed", claim_id, seed)
        cases.append({
            "failure_mode": mode,
            "shape": shape,
            "claim_id": claim_id,
            "seed": seed,
            "bug_switches": list(bugs),
            "control_run_id": controls[key]["trial"]["result"]["run_id"],
            **case,
        })
    # Replay every v1 item as a control, including missing-info and ownership
    # cases. A mode tag describes what an item exercises, not an observed failure.
    for claim in load_jsonl(SOURCE):
        key = (claim["claim_id"], 11)
        if key not in controls:
            controls[key] = investigate("fixed", *key)
    return {
        "run_id": f"M1-trace-{sha12(SOURCE)}",
        "source": {"claims": str(SOURCE), "claims_sha": sha12(SOURCE),
                   "world_sha": sha12(Path("data/public_world_state.json")),
                   "label_source": "public_claims.expected via lab9.trace_case.investigate"},
        "note": "Public trace evidence only; M3 graders and the M4 baseline are not run here.",
        "cases": cases,
        "controls": list(controls.values()),
    }


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="reports/m1_trace_evidence.json")
    args = parser.parse_args(argv)
    report = collect()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report["run_id"])
    for case in report["cases"]:
        trial = case["trial"]
        verdict = "PASS" if trial["lab8_pass"] else "FAIL"
        print(f"{case['failure_mode']} {case['shape']} {case['claim_id']}@{case['seed']}: "
              f"Lab 8 {verdict} ({trial['lab8_reason']}); "
              f"ledger={trial['snapshot']['refund_vnd']}")
    print(f"fixed controls: {sum(c['trial']['lab8_pass'] for c in report['controls'])}"
          f"/{len(report['controls'])} PASS")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
