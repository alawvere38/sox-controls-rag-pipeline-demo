"""Run the golden eval set against the live agent, score it, and write a report.

Usage:
    python3 -m evals.run_evals                          # full dataset, judges on
    python3 -m evals.run_evals --no-judge               # deterministic checks only
    python3 -m evals.run_evals --ids sc-01 oos-01
    python3 -m evals.run_evals --baseline evals/baseline.json   # exit 1 on regressions

Each run writes evals/runs/run-<UTC timestamp>.json (full data) and a sibling .md report.
To pin the current behavior as the baseline: cp evals/runs/run-<ts>.json evals/baseline.json
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from evals.adapter import query_agent
from evals.report import build_markdown, diff_against_baseline, summarize
from evals.scoring import score_item

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = REPO_ROOT / "evals" / "dataset.jsonl"
RUNS_DIR = REPO_ROOT / "evals" / "runs"


def load_dataset(path: Path) -> list:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the SOX RAG eval suite")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--ids", nargs="*", help="only run these item ids")
    parser.add_argument("--limit", type=int, help="only run the first N items")
    parser.add_argument("--sleep", type=float, default=1.0, help="seconds between agent calls")
    parser.add_argument("--no-judge", action="store_true", help="skip the LLM judges")
    parser.add_argument("--baseline", type=Path, help="diff against this run; exit 1 on regressions")
    args = parser.parse_args()

    items = load_dataset(args.dataset)
    if args.ids:
        items = [i for i in items if i["id"] in args.ids]
    if args.limit:
        items = items[: args.limit]
    if not items:
        print("no items selected", file=sys.stderr)
        return 1

    started = datetime.now(timezone.utc)
    results = []
    for n, item in enumerate(items, start=1):
        try:
            response = query_agent(item["question"])
            scored = score_item(item, response, use_judge=not args.no_judge)
            error = None
            verdict = "PASS" if scored["pass"] else "FAIL"
        except Exception as exc:  # keep the run going; record the failure
            response, scored, error, verdict = None, None, str(exc), "ERROR"
        print(f"[{n}/{len(items)}] {verdict}  {item['id']}  {item['question']}")
        if error:
            print(f"        {error}", file=sys.stderr)
        results.append({"item": item, "response": response, "scored": scored, "error": error})
        if n < len(items):
            time.sleep(args.sleep)

    run = {
        "created_at": started.isoformat(),
        "dataset": str(args.dataset.relative_to(REPO_ROOT)),
        "judge": not args.no_judge,
        "item_count": len(results),
        "errors": sum(1 for r in results if r["error"]),
        "results": results,
    }
    RUNS_DIR.mkdir(exist_ok=True)
    out_path = RUNS_DIR / f"run-{started.strftime('%Y%m%dT%H%M%SZ')}.json"
    out_path.write_text(json.dumps(run, indent=2))
    out_path.with_suffix(".md").write_text(build_markdown(run))

    s = summarize(run)
    print(f"\noverall: {s['passed']}/{s['total']} passed")
    for cat in sorted(s["by_category"]):
        c = s["by_category"][cat]
        print(f"  {cat}: {c['passed']}/{c['total']}")
    print(f"saved: {out_path} (+ .md report)")

    if args.baseline:
        delta = diff_against_baseline(run, json.loads(args.baseline.read_text()))
        print(f"baseline diff: regressions={delta['regressions'] or 'none'} "
              f"improvements={delta['improvements'] or 'none'}")
        if delta["regressions"]:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
