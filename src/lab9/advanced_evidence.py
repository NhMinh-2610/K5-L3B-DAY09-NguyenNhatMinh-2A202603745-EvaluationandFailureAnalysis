"""Reproduce M5-M7 evidence using the provided eval, mutation, traps and gate CLIs.

Run from src/: python -m lab9.advanced_evidence
Reports are generated, never repaired in place. Diagnostic shapes only register
existing switches in memory; they do not change Lab 8 or the supplied variants.
"""
from __future__ import annotations

from contextlib import redirect_stdout
import copy
import io
import json
from pathlib import Path
import tempfile

from lab8.console import utf8_stdio
from lab8.shapes import SHAPES
from lab9 import eval as evaluation, evalset, gate, mutation, traps, variants
from lab9.variant_agent import make_shape

SPEC = "config/metric_spec_v2.yaml"
BASE = "reports/baseline_v2.json"


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def capture(main, args: list[str], log: str, expected: int, checks: list):
    output = io.StringIO()
    with redirect_stdout(output):
        code = main(args)
    text = output.getvalue()
    path = Path(log)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    checks.append({"module": main.__module__, "args": args, "exit_code": code,
                   "expected_exit_code": expected, "log": log})
    print(f"{main.__module__}: exit {code} (expected {expected}); {log}", flush=True)
    if code != expected:
        raise RuntimeError(f"Unexpected exit {code}: see {log}\n{text}")


def trace_evidence(spec):
    variants.register()
    world, claims = evaluation.load_world(spec)
    labels = json.loads(Path(spec["labels"]).read_text(encoding="utf-8"))
    cases = [("fixed", "C-110"), ("fixed", "C-113"), ("fixed", "C-114"),
             ("v2_misreport", "C-109"), ("fixed", "C-109"),
             ("v2_quiet_override", "C-101"), ("fixed", "C-101")]
    collected = []
    with tempfile.TemporaryDirectory(prefix="lab9-v2-trace-", ignore_cleanup_errors=True) as tmp:
        for shape, claim in cases:
            trial = evaluation.make_task(shape, world, claims, labels, Path(tmp))(
                {"claim_id": claim, "seed": 11})
            collected.append({"shape": shape, "claim_id": claim, "seed": 11,
                              "label": labels[claim], "trial": trial})
    return {"run_id": f"M5-M7-trace-{evalset.sha12(Path(spec['eval_set']))}",
            "note": "Public diagnostics and negative controls; not instructor hidden tests.",
            "cases": collected}


def submission_evidence():
    sections = ["# Bằng chứng để dán vào PR Lab 9\n\n"
                "Đây là kết quả chạy local do trợ lý thực hiện theo sự đồng ý của chủ fork. "
                "Theo yêu cầu mới của chủ fork, trợ lý commit/push, tạo PR trong fork, "
                "theo dõi CI và chỉ merge khi xanh. "
                "Chưa chạy GitHub CI hoặc bộ chấm ẩn.\n"]
    for title, path in (
        ("Core: seeded_regression bị chặn, exit 1", "reports/gate_seeded_regression_after_m7.txt"),
        ("M5–M7: scorecard chính thức, exit 0", "reports/mutation_v2.txt"),
        ("M6: A/A, exit 0", "reports/aa_v2.txt"),
        ("M7: bốn trap công khai, lệnh traps exit 0", "reports/traps_v2.txt"),
        *((f"Gate trap {name}, exit 1", f"reports/traps/{name}.gate.txt") for name in (
            "evaluator_errors_as_nan", "dropped_failing_rows", "cherry_picked_seeds", "loosened_spec")),
    ):
        log_text = "\n".join(line.rstrip() for line in Path(path).read_text(encoding='utf-8').splitlines())
        sections.append(f"\n## {title}\n\n```text\n{log_text}\n```\n")
    sections.append("\nGiới hạn: MockLLM, 28 item v2, năm seed và judge replay công khai; "
                    "bug chỉ xuất hiện ở 1/3 seed chưa được phát hiện ổn định với cỡ mẫu này. "
                    "Các vector kiểm tra bổ sung do trợ lý tạo không phải test ẩn của giảng viên.\n")
    Path("../docs/PR_LAB9.md").write_text("".join(sections), encoding="utf-8")


def main() -> int:
    utf8_stdio()
    checks = []
    spec = evaluation.load_spec(Path(SPEC))
    Path("reports").mkdir(exist_ok=True)
    Path("reports/metric_spec_v2.baseline.yaml").write_text(
        Path(SPEC).read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    capture(evaluation.main, ["--shape", "swarm", "--spec", SPEC, "--out", BASE],
            "reports/baseline_v2.txt", 0, checks)
    for shape in ("fixed", "honest_refactor", "seeded_regression", "slice_regression", "flaky_regression"):
        suffix = "_v2" if shape in {"fixed", "honest_refactor", "seeded_regression"} else ""
        capture(evaluation.main, ["--shape", shape, "--spec", SPEC,
                                 "--out", f"reports/eval_{shape}{suffix}.json"],
                f"reports/eval_{shape}{suffix}.txt", 0, checks)
    capture(mutation.main, ["--spec", SPEC, "--aa", "66,77,88,99,110"],
            "reports/aa_v2.txt", 0, checks)
    capture(mutation.main, ["--spec", SPEC, "--baseline", BASE],
            "reports/mutation_v2.txt", 0, checks)
    for name, bugs in (("v2_misreport", {"no_override", "misreport"}),
                       ("v2_quiet_override", {"no_override", "quiet_override"})):
        SHAPES[name] = make_shape(name, frozenset(bugs))
        capture(evaluation.main, ["--shape", name, "--spec", SPEC,
                                 "--out", f"reports/eval_{name}.json"],
                f"reports/eval_{name}.txt", 0, checks)
    for name, suffix, expected in (("swarm", "", 0), ("fixed", "_v2", 0),
                                    ("honest_refactor", "_v2", 0),
                                    ("seeded_regression", "_v2", 1),
                                    ("slice_regression", "", 1), ("flaky_regression", "", 1),
                                    ("v2_misreport", "", 1), ("v2_quiet_override", "", 1)):
        report = BASE if name == "swarm" else f"reports/eval_{name}{suffix}.json"
        capture(gate.main, ["--pr", report, "--baseline", BASE, "--spec", SPEC,
                            "--base-spec", "reports/metric_spec_v2.baseline.yaml"],
                f"reports/gate_{name}_v2.txt", expected, checks)
    capture(traps.main, ["--pr", "reports/eval_slice_regression.json", "--baseline", BASE,
                         "--spec", SPEC], "reports/traps_v2.txt", 0, checks)
    for name in ("evaluator_errors_as_nan", "dropped_failing_rows", "cherry_picked_seeds", "loosened_spec"):
        args = ["--pr", f"reports/traps/{name}.json", "--baseline", BASE, "--spec",
                f"reports/traps/{name}.spec.yaml" if name == "loosened_spec" else SPEC]
        if name == "loosened_spec":
            args += ["--base-spec", SPEC]
        capture(gate.main, args, f"reports/traps/{name}.gate.txt", 1, checks)

    # Own attack vectors, distinct from the unavailable instructor hidden set.
    base = json.loads(Path(BASE).read_text(encoding="utf-8"))
    for name in ("duplicate_row", "evaluator_failure_green", "relabel_slice", "forged_summary"):
        report = copy.deepcopy(base)
        if name == "duplicate_row":
            report["rows"][0] = copy.deepcopy(report["rows"][1])
        elif name == "evaluator_failure_green":
            report["evaluator_failures"] = ["Synthetic: grader failed on an otherwise green run"]
        elif name == "relabel_slice":
            item = next(r["item_id"] for r in report["rows"] if "money_movement" in r["slices"])
            for row in report["rows"]:
                if row["item_id"] == item:
                    row["slices"] = []
        else:
            report["metrics"]["pass_rate"] = 1.0
        path = f"reports/extra_traps/{name}.json"
        write_json(Path(path), report)
        capture(gate.main, ["--pr", path, "--baseline", BASE, "--spec", SPEC],
                f"reports/extra_traps/{name}.gate.txt", 1, checks)
    for name, expected in (("pr", 0), ("fixed", 0), ("seeded_regression", 1)):
        capture(gate.main, ["--pr", f"reports/eval_{name}.json", "--baseline", "reports/baseline_v1.json",
                            "--spec", "config/metric_spec.yaml"],
                f"reports/gate_{name}_after_m7.txt", expected, checks)
    write_json(Path("reports/v2_trace_evidence.json"), trace_evidence(spec))
    write_json(Path("reports/advanced_checks.json"), {
        "run_id": f"M5-M7-{base['manifest']['eval_set_sha']}",
        "note": "Local evidence only; no GitHub CI or instructor hidden tests were run.",
        "checks": checks})
    submission_evidence()
    print(f"Completed {len(checks)} CLI checks and v2 trace evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
