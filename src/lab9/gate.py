"""CI gate: compare a PR eval report with the main-branch baseline using the metric spec.

    python -m lab9.gate --pr reports/eval_workflow.json --baseline reports/baseline_v1.json

exit 0 = merge, exit 1 = blocked. Safety metrics: max 0, no averaging away.
Capability metrics: meet the floor AND the paired CI of (PR - main) is not entirely below 0.
Thresholds may only get stricter on the same eval-set version (ratchet).
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from math import isclose, isfinite
from numbers import Integral, Real
from pathlib import Path
import re

from lab8.console import utf8_stdio
from lab9 import stats
from lab9.eval import SPEC, load_spec, per_item
from lab9.graders import GRADERS


def _finite(value) -> bool:
    try:
        return isinstance(value, Real) and isfinite(value)
    except (OverflowError, TypeError):
        return False


def _derived(metric: str) -> bool:
    return metric in {"pass_5", "cost_per_success"} or bool(re.fullmatch(r"pass_(at|hat)_\d+", metric))


def _spec_problems(spec: dict) -> list[str]:
    if not isinstance(spec, dict) or not isinstance(spec.get("metrics"), list) or not spec["metrics"]:
        return ["spec: metrics must be a non-empty list"]
    problems, ids = [], []
    for metric in spec["metrics"]:
        if not isinstance(metric, dict) or not isinstance(metric.get("id"), str):
            problems.append("spec: invalid metric definition")
            continue
        ids.append(metric["id"])
        if not isinstance(metric.get("threshold", {}), dict):
            problems.append(f"spec: invalid threshold for {metric['id']}")
            continue
        for key in ("min", "max", "max_increase"):
            if key in metric.get("threshold", {}) and not _finite(metric["threshold"][key]):
                problems.append(f"spec: non-finite {metric['id']}/{key}")
    if len(set(ids)) != len(ids):
        problems.append("spec: duplicate metric id")
    slices = spec.get("slices", [])
    if not isinstance(slices, list):
        return problems + ["spec: slices must be a list"]
    keys = []
    for entry in slices:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or not isinstance(entry.get("metric"), str):
            problems.append("spec: invalid slice definition")
            continue
        keys.append((entry["name"], entry["metric"]))
        if "min" in entry and not _finite(entry["min"]):
            problems.append(f"spec: non-finite slice floor {entry['name']}")
    if len(set(keys)) != len(keys):
        problems.append("spec: duplicate slice definition")
    return problems


def _ratchet(spec: dict, base_spec: dict) -> list[str]:
    if spec.get("eval_set_version") != base_spec.get("eval_set_version"):
        return []
    problems = []

    def thresholds(label, current, previous):
        for key in ("min", "max", "max_increase"):
            if key not in previous:
                continue
            value = current.get(key)
            if (not _finite(value) or (key == "min" and value < previous[key])
                    or (key != "min" and value > previous[key])):
                problems.append(f"ratchet: {label}/{key} was removed or loosened")
        if previous.get("no_significant_drop") and not current.get("no_significant_drop"):
            problems.append(f"ratchet: {label}/no_significant_drop was removed")

    current_metrics = {m["id"]: m for m in spec["metrics"]}
    for old in base_spec["metrics"]:
        new = current_metrics.get(old["id"])
        if new is None:
            problems.append(f"ratchet: metric {old['id']} disappeared")
            continue
        if old.get("blocking") and not new.get("blocking"):
            problems.append(f"ratchet: metric {old['id']} is no longer blocking")
        thresholds(old["id"], new.get("threshold", {}), old.get("threshold", {}))
    current_slices = {(s["name"], s["metric"]): s for s in spec.get("slices", [])}
    for old in base_spec.get("slices", []):
        label = f"slice:{old['name']}/{old['metric']}"
        new = current_slices.get((old["name"], old["metric"]))
        if new is None:
            problems.append(f"ratchet: {label} disappeared")
            continue
        if old.get("blocking") and not new.get("blocking"):
            problems.append(f"ratchet: {label} is no longer blocking")
        thresholds(label, new, old)
    return problems


def _report_integrity(report: dict, spec: dict, label: str):
    problems, pairs, tags = [], set(), {}
    if not isinstance(report, dict):
        return [f"{label}: report must be an object"], pairs, tags
    manifest, rows, metrics = report.get("manifest"), report.get("rows"), report.get("metrics")
    if not isinstance(manifest, dict) or not isinstance(rows, list) or not isinstance(metrics, dict):
        return [f"{label}: missing manifest, rows or metrics"], pairs, tags
    if not isinstance(report.get("evaluator_failures"), list) or report["evaluator_failures"]:
        problems.append(f"{label}: evaluator_failures is missing or non-empty")
    if not isinstance(manifest.get("eval_set_sha"), str) or not manifest["eval_set_sha"]:
        problems.append(f"{label}: missing eval_set_sha")
    n, seeds = manifest.get("items"), manifest.get("seeds")
    if isinstance(n, bool) or not isinstance(n, Integral) or n < 1:
        problems.append(f"{label}: invalid manifest item count")
    if (not isinstance(seeds, list) or not seeds
            or any(isinstance(s, bool) or not isinstance(s, Integral) for s in seeds)
            or len(set(seeds)) != len(seeds)):
        return problems + [f"{label}: invalid or duplicate manifest seeds"], pairs, tags
    if "seeds" in spec and set(seeds) != set(spec["seeds"]):
        problems.append(f"{label}: manifest seeds differ from spec")
    if "metric_spec_version" in spec and manifest.get("metric_spec_version") != spec["metric_spec_version"]:
        problems.append(f"{label}: metric_spec_version differs from spec")
    if isinstance(n, Integral) and len(rows) != n * len(seeds):
        problems.append(f"{label}: row count does not equal manifest items x seeds")
    for mid, value in metrics.items():
        if value is not None and not _finite(value):
            problems.append(f"{label}: non-finite or invalid metric {mid}")
    for metric in spec["metrics"]:
        mid = metric["id"]
        if mid not in metrics or (metrics[mid] is None and mid != "cost_per_success"):
            problems.append(f"{label}: missing metric {mid}")
    graded = [m for m in spec["metrics"] if not _derived(m["id"]) and m.get("kind") != "system"]
    values = defaultdict(list)
    passes = defaultdict(list)
    costs, usable = [], True
    pair_counts = Counter()
    for row in rows:
        if not isinstance(row, dict):
            problems.append(f"{label}: non-object row")
            usable = False
            continue
        item, seed = row.get("item_id"), row.get("seed")
        if not isinstance(item, str) or not item or isinstance(seed, bool) or not isinstance(seed, Integral):
            problems.append(f"{label}: invalid row item_id/seed")
            usable = False
            continue
        pair_counts[item, seed] += 1
        pairs.add((item, seed))
        slice_tags = row.get("slices", [])
        if not isinstance(slice_tags, list) or any(not isinstance(t, str) for t in slice_tags):
            problems.append(f"{label}: invalid slice tags for {item}")
            usable = False
        else:
            item_tags = frozenset(slice_tags)
            if len(item_tags) != len(slice_tags) or (item in tags and tags[item] != item_tags):
                problems.append(f"{label}: inconsistent slice tags for {item}")
            tags[item] = item_tags
        for metric in graded:
            mid, value = metric["id"], row.get(metric["id"])
            if (not _finite(value) or not 0 <= value <= 1
                    or (mid in GRADERS and value not in (0, 1))):
                problems.append(f"{label}: missing/invalid row value {mid} at {item}@{seed}")
                usable = False
            else:
                values[mid].append(float(value))
        if row.get("pass_rate") in (True, False, 0, 1):
            passes[item].append(bool(row["pass_rate"]))
        if "cost" in row:
            if not _finite(row["cost"]) or row["cost"] < 0:
                problems.append(f"{label}: invalid row cost at {item}@{seed}")
                usable = False
            else:
                costs.append(float(row["cost"]))
    if any(count != 1 for count in pair_counts.values()):
        problems.append(f"{label}: duplicate (item_id, seed) rows")
    items = {item for item, _ in pairs}
    if len(items) != n or pairs != {(item, seed) for item in items for seed in seeds}:
        problems.append(f"{label}: incomplete item x seed grid")
    if not usable or not rows:
        return problems, pairs, tags

    def compare(mid, expected):
        if mid not in metrics:
            return
        actual = metrics[mid]
        if expected is None:
            if actual is not None:
                problems.append(f"{label}: summary {mid} disagrees with rows")
        elif not _finite(actual) or not isclose(actual, expected, rel_tol=0, abs_tol=0.000051):
            problems.append(f"{label}: summary {mid} disagrees with rows")

    for metric in graded:
        mid, vals = metric["id"], values[metric["id"]]
        expected = sum(vals) if metric.get("kind") == "safety" else round(sum(vals) / len(vals), 4)
        compare(mid, expected)
    if passes:
        compare("pass_5", round(sum(all(v) for v in passes.values()) / len(passes), 4))
        for mid in metrics:
            match = re.fullmatch(r"pass_(at|hat)_(\d+)", str(mid))
            if match:
                fn = stats.pass_at_k if match[1] == "at" else stats.pass_hat_k
                k = int(match[2])
                try:
                    expected = sum(fn(len(v), sum(v), k) for v in passes.values()) / len(passes)
                    compare(mid, round(expected, 4))
                except ValueError:
                    problems.append(f"{label}: undefined {mid} for the row counts")
        if "cost_per_success" in metrics:
            if len(costs) != len(rows):
                problems.append(f"{label}: missing row costs")
            else:
                successes = sum(sum(v) for v in passes.values())
                compare("cost_per_success", round(sum(costs) / successes, 4) if successes else None)
    return problems, pairs, tags


def integrity_check(pr: dict, base: dict, spec: dict, base_spec: dict | None = None) -> list[str]:
    """M7 (Expert): refuse to compare reports that cannot be trusted. Return a list of problems
    (empty = trustworthy). A gate that passes a broken report is worse than no gate.
    Must catch at least:
      - any metric value in pr["metrics"] that is NaN or inf
      - len(pr["rows"]) != manifest items x len(manifest seeds)   (dropped / duplicated rows)
      - the (item_id, seed) set of PR differs from the baseline's (cherry-picked seeds/items)
      - pr["evaluator_failures"] non-empty, or a row whose value for a graded spec metric is
        None (a crashed grader silently scores as "missing" and drops out of the mean)
      - base_spec given and a threshold in spec is LOOSER than in base_spec for the same
        eval-set version (ratchet: max may not rise, min may not fall, a blocking metric may
        not become non-blocking, a metric may not disappear; the same for spec["slices"],
        including dropping no_significant_drop)
      - an item's slice tags in PR rows differ from the baseline's (relabelling an item out of a
        slice hides its regression from the slice gate)"""
    problems = _spec_problems(spec)
    if base_spec is not None:
        problems += _spec_problems(base_spec)
    if problems:
        return problems
    pr_problems, pr_pairs, pr_tags = _report_integrity(pr, spec, "PR")
    base_problems, base_pairs, base_tags = _report_integrity(base, base_spec or spec, "baseline")
    problems += pr_problems + base_problems
    if pr_pairs != base_pairs:
        problems.append("PR (item_id, seed) set differs from baseline")
    if pr_tags != base_tags:
        problems.append("PR item slice tags differ from baseline")
    if base_spec is not None:
        problems += _ratchet(spec, base_spec)
    return list(dict.fromkeys(problems))


def slice_check(pr: dict, base: dict, spec: dict) -> tuple[list[str], list[str]]:
    """M5 (Advanced): an average can hide a regression on a small, important slice.
    For each entry of spec["slices"] ({"name", "metric", "min"?, "no_significant_drop"?, "blocking"}):
      - value = mean of per_item(pr, metric, slice_name=name)
      - fail if below "min", or if no_significant_drop and the paired CI over the slice's items
        lies entirely below 0
    Return (blocked ids like "slice:money_movement/pass_rate", report lines)."""
    blocked, lines = [], []
    bs = spec.get("bootstrap", {})
    for entry in spec.get("slices", []):
        name, metric = entry["name"], entry["metric"]
        sid = f"slice:{name}/{metric}"
        a, b = per_item(pr, metric, slice_name=name), per_item(base, metric, slice_name=name)
        value = sum(a.values()) / len(a) if a else None
        failed, note = value is None, ""
        if value is not None and "min" in entry and value < entry["min"]:
            failed = True
        if set(a) != set(b):
            failed, note = True, "slice items differ from baseline"
        elif entry.get("no_significant_drop") and a:
            keys = sorted(a)
            try:
                delta, lo, hi = stats.paired_bootstrap(
                    [a[k] for k in keys], [b[k] for k in keys],
                    n_resamples=bs.get("n_resamples", 1000), rng=bs.get("rng", 2027),
                    confidence=bs.get("confidence", 0.95))
                note = f"Δ {delta:+.3f} CI [{lo:+.3f}, {hi:+.3f}]"
                failed |= hi < 0
            except ValueError as exc:
                failed, note = True, f"cannot compute slice CI: {exc}"
        if failed and entry.get("blocking"):
            blocked.append(sid)
        verdict = "BLOCK" if failed and entry.get("blocking") else "warn" if failed else "ok"
        lines.append(f"  {sid} {value!s} min={entry.get('min')} {note} {verdict}")
    return blocked, lines


def check(pr: dict, base: dict, spec: dict, base_spec: dict | None = None) -> tuple[list[str], list[str]]:
    problems = integrity_check(pr, base, spec, base_spec)
    if problems:
        return ["integrity"], [f"  INTEGRITY {p}" for p in problems]
    if pr["manifest"]["eval_set_sha"] != base["manifest"]["eval_set_sha"]:
        return ["eval_set_sha"], ["  EVAL SET differs from the baseline's: re-run the baseline on the same eval set"]
    blocked, lines = [], []
    bs = spec.get("bootstrap", {})
    for m in spec["metrics"]:
        mid, th, val = m["id"], m.get("threshold", {}), pr["metrics"].get(m["id"])
        verdict, note = "ok", ""
        if val is None:
            verdict = "missing"
        elif "max" in th and val > th["max"]:
            verdict = "fail"
        elif "min" in th and val < th["min"]:
            verdict = "fail"
        elif "max_increase" in th and base["metrics"].get(mid):
            if val > base["metrics"][mid] * (1 + th["max_increase"]):
                verdict = "fail"
        if th.get("no_significant_drop") and val is not None:
            a, b = per_item(pr, mid), per_item(base, mid)
            keys = sorted(set(a) & set(b))
            d, lo, hi = stats.paired_bootstrap([a[k] for k in keys], [b[k] for k in keys],
                                               n_resamples=bs.get("n_resamples", 1000), rng=bs.get("rng", 2027),
                                               confidence=bs.get("confidence", 0.95))
            note = f"Δ {d:+.3f} CI [{lo:+.3f}, {hi:+.3f}]"
            if hi < 0:
                verdict = "fail"
        if verdict != "ok" and m.get("blocking"):
            blocked.append(mid)
        label = {"ok": "ok", "missing": "MISSING"}.get(verdict, "BLOCK" if m.get("blocking") else "warn")
        lines.append(f"  {mid:<22} {val!s:<8} {json.dumps(th):<40} {note:<28} {label}")
    if spec.get("slices"):
        sb, sl = slice_check(pr, base, spec)
        blocked += sb
        lines += sl
    return blocked, lines


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(prog="lab9.gate")
    ap.add_argument("--pr", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--spec", default=str(SPEC))
    ap.add_argument("--base-spec", help="metric spec on main, for the ratchet check (M7)")
    args = ap.parse_args(argv)
    pr = json.loads(Path(args.pr).read_text(encoding="utf-8"))
    base = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    base_spec = load_spec(Path(args.base_spec)) if args.base_spec else None
    blocked, lines = check(pr, base, load_spec(Path(args.spec)), base_spec)
    pr_meta = pr if isinstance(pr, dict) else {}
    base_meta = base if isinstance(base, dict) else {}
    manifest = pr_meta.get("manifest")
    fingerprint = manifest.get("eval_set_sha", "<missing>") if isinstance(manifest, dict) else "<missing>"
    print(f"gate: PR {pr_meta.get('run_id', '<missing>')} vs main {base_meta.get('run_id', '<missing>')} · eval set {fingerprint}")
    print("\n".join(lines))
    if blocked:
        print(f"exit 1 — blocked: {', '.join(blocked)}")
        return 1
    print("exit 0 — merge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
