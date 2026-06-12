"""Report writer for eval runs: per-item pass/fail, per-category and per-check
aggregates, and regression diffing against a baseline run.

CLI:
    python -m evals.report evals/runs/run-<ts>.json
    python -m evals.report evals/runs/run-<ts>.json --baseline evals/baseline.json
"""

import argparse
import json
import sys
from pathlib import Path


def _item_row(result: dict) -> dict:
    scored = result.get("scored")
    failed_checks = []
    if scored:
        failed_checks = [name for name, s in scored["scores"].items() if not s["pass"]]
    return {
        "id": result["item"]["id"],
        "category": result["item"]["category"],
        "pass": bool(scored and scored["pass"]),
        "failed_checks": failed_checks,
        "error": result.get("error"),
    }


def summarize(run: dict) -> dict:
    rows = [_item_row(r) for r in run["results"]]

    by_category = {}
    for row in rows:
        cat = by_category.setdefault(row["category"], {"passed": 0, "total": 0})
        cat["total"] += 1
        cat["passed"] += row["pass"]

    by_check = {}
    for result in run["results"]:
        for name, score in (result.get("scored") or {}).get("scores", {}).items():
            check = by_check.setdefault(name, {"passed": 0, "total": 0})
            check["total"] += 1
            check["passed"] += bool(score["pass"])

    return {
        "passed": sum(r["pass"] for r in rows),
        "total": len(rows),
        "by_category": by_category,
        "by_check": by_check,
        "items": rows,
    }


def build_markdown(run: dict) -> str:
    s = summarize(run)
    lines = [
        "# Eval run report",
        "",
        f"- Created: {run['created_at']}",
        f"- Dataset: {run['dataset']}",
        f"- Errors: {run['errors']}",
        "",
        f"## Overall: {s['passed']}/{s['total']} passed",
        "",
        "## By category",
        "",
        "| Category | Passed |",
        "|---|---|",
    ]
    for cat in sorted(s["by_category"]):
        c = s["by_category"][cat]
        lines.append(f"| {cat} | {c['passed']}/{c['total']} |")
    lines += ["", "## By check", "", "| Check | Passed |", "|---|---|"]
    for name in sorted(s["by_check"]):
        c = s["by_check"][name]
        lines.append(f"| {name} | {c['passed']}/{c['total']} |")
    lines += ["", "## Items", "", "| Item | Category | Result | Failed checks |", "|---|---|---|---|"]
    for row in s["items"]:
        result = "ERROR" if row["error"] else ("PASS" if row["pass"] else "FAIL")
        lines.append(f"| {row['id']} | {row['category']} | {result} | {', '.join(row['failed_checks']) or '—'} |")
    return "\n".join(lines) + "\n"


def diff_against_baseline(run: dict, baseline: dict) -> dict:
    current = {r["item"]["id"]: bool(r.get("scored") and r["scored"]["pass"]) for r in run["results"]}
    base = {r["item"]["id"]: bool(r.get("scored") and r["scored"]["pass"]) for r in baseline["results"]}
    shared = set(current) & set(base)
    return {
        "regressions": sorted(i for i in shared if base[i] and not current[i]),
        "improvements": sorted(i for i in shared if not base[i] and current[i]),
        "only_in_run": sorted(set(current) - set(base)),
        "only_in_baseline": sorted(set(base) - set(current)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an eval run report")
    parser.add_argument("run", type=Path)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()

    run = json.loads(args.run.read_text())
    print(build_markdown(run))

    if args.baseline:
        delta = diff_against_baseline(run, json.loads(args.baseline.read_text()))
        print("## Baseline diff\n")
        for key in ("regressions", "improvements", "only_in_run", "only_in_baseline"):
            print(f"- {key}: {', '.join(delta[key]) or 'none'}")
        if delta["regressions"]:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
