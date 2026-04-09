#!/usr/bin/env python3
"""
run_all.py — Execute all new_bench benchmarks and report results.

Usage:
    # Direct LLM mode (no RAG), all datasets
    python -m new_bench.run_all

    # DrugClaw simple thinking mode
    python -m new_bench.run_all --mode simple

    # DrugClaw full graph thinking mode
    python -m new_bench.run_all --mode graph

    # Limit samples per dataset
    python -m new_bench.run_all --max-samples 50

    # Run specific datasets
    python -m new_bench.run_all --datasets drug_qa medqa twosides

    # Exclude dataset's own skill from RAG retrieval (maskself)
    python -m new_bench.run_all --mode simple --maskself

    # Save results and logs
    python -m new_bench.run_all --output results.json --log-dir ./bench_logs

    # DDInter: run severity + binary subtasks
    python -m new_bench.run_all --datasets ddinter --ddinter-task both

Modes:
    direct  — Pure LLM inference, no retrieval (default)
    simple  — DrugClaw RAG with simple (one-shot) thinking mode
    graph   — DrugClaw RAG with full multi-agent graph thinking mode
"""

import argparse
import importlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent

# ── Defaults (logs are always written) ───────────────────────────────────
from new_bench.bench_utils import DEFAULT_LOG_DIR

ALL_DATASETS = [
    "drug_qa",
    "medqa",
    "phee_extract",
    "repodb",
    "twosides",
    "ddinter",
    "gdsc",
]

# Primary metric name per dataset (used in summary)
PRIMARY_METRIC: dict[str, str] = {
    "drug_qa":      "accuracy",
    "medqa":        "accuracy",
    "phee_extract": "micro_f1",
    "repodb":       "mrr",
    "twosides":     "f1_macro",
    "ddinter":      "f1_macro",     # severity task default
    "gdsc":         "accuracy",
}


def _fmt_result(ds: str, res: dict) -> str:
    """Format a single result line for the summary table."""
    if "error" in res:
        return f"  {ds:20s}  ERROR: {res['error']}"

    parts = []
    metric = PRIMARY_METRIC.get(ds, "accuracy")

    # Classification / extraction metrics
    if metric in res:
        parts.append(f"{metric.upper()}={res[metric]}")

    # Secondary metrics
    for key in ("f1_macro", "micro_f1", "precision", "recall", "auroc",
                "mrr", "ndcg@20", "recall@10", "recall@50"):
        if key in res and key != metric:
            parts.append(f"{key}={res[key]}")

    n = res.get("total") or res.get("total_queries") or "?"
    parts.append(f"N={n}")
    return f"  {ds:20s}  {' | '.join(parts)}"


def run_one(
    dataset: str,
    key_file: str | None,
    max_samples: int,
    mode: str,
    maskself: bool,
    log_dir: str | None,
    ddinter_task: str,
) -> dict:
    """Import and run a single dataset benchmark, return its results dict."""
    mod = importlib.import_module(f"new_bench.{dataset}.bench")
    kwargs: dict = dict(
        key_file=key_file,
        max_samples=max_samples,
        mode=mode,
        maskself=maskself,
        log_dir=log_dir,
    )
    if dataset == "ddinter":
        kwargs["task"] = ddinter_task
    return mod.run(**kwargs)


def main():
    parser = argparse.ArgumentParser(
        description="DrugClaw new-bench runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--datasets", nargs="+", default=ALL_DATASETS,
        help="Dataset names to run (default: all)",
    )
    parser.add_argument(
        "--mode", type=str, default="direct",
        choices=["direct", "simple", "graph"],
        help=(
            "Inference mode: "
            "'direct'=pure LLM (default), "
            "'simple'=DrugClaw RAG simple thinking, "
            "'graph'=DrugClaw RAG full graph thinking"
        ),
    )
    parser.add_argument(
        "--maskself", action="store_true", default=False,
        help=(
            "Exclude the dataset's own skill from RAG retrieval "
            "(only applies to simple/graph modes)"
        ),
    )
    parser.add_argument(
        "--max-samples", type=int, default=0,
        help="Max samples per dataset (0 = all available)",
    )
    parser.add_argument(
        "--key-file", type=str, default=None,
        help="Path to API key JSON file (auto-detected if omitted)",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help=(
            "Path to write JSON results file "
            "(default: <log-dir>/results_<timestamp>.json)"
        ),
    )
    parser.add_argument(
        "--log-dir", type=str, default=DEFAULT_LOG_DIR,
        help=f"Directory to save per-sample logs (default: {DEFAULT_LOG_DIR})",
    )
    parser.add_argument(
        "--ddinter-task", type=str, default="severity",
        choices=["severity", "binary", "both"],
        help="DDInter sub-task: severity (default), binary, or both",
    )
    args = parser.parse_args()

    # Resolve output path — always write, even if not explicitly set
    ts_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = args.output or str(
        Path(args.log_dir) / f"results_{ts_now}.json"
    )

    print(f"\nMode: {args.mode.upper()}"
          + (" + maskself" if args.maskself and args.mode != "direct" else ""))
    print(f"Max samples: {args.max_samples or 'all'}")
    print(f"Log dir:     {args.log_dir}")
    print(f"Results:     {output_path}")

    all_results: dict = {}
    for ds in args.datasets:
        if ds not in ALL_DATASETS:
            print(f"[WARN] Unknown dataset '{ds}', skipping.")
            continue

        print(f"\n{'='*62}")
        print(f"  Benchmarking: {ds}")
        print(f"{'='*62}")
        t0 = time.time()
        try:
            result = run_one(
                ds,
                args.key_file,
                args.max_samples,
                args.mode,
                args.maskself,
                args.log_dir,
                args.ddinter_task,
            )
            result["elapsed_sec"] = round(time.time() - t0, 1)
            all_results[ds] = result

            # Per-dataset pretty print
            for key, val in result.items():
                if key not in ("per_class", "elapsed_sec") and not isinstance(val, dict):
                    print(f"  {key}: {val}")
            print(f"  Time: {result['elapsed_sec']}s")

        except Exception as e:
            import traceback
            print(f"  [ERROR] {e}")
            traceback.print_exc()
            all_results[ds] = {"error": str(e)}

    # ── Summary table ─────────────────────────────────────────────────
    print(f"\n{'='*62}")
    print("  SUMMARY")
    print(f"{'='*62}")
    for ds, res in all_results.items():
        # ddinter "both" returns nested dicts
        if isinstance(res.get("severity"), dict) or isinstance(res.get("binary"), dict):
            for sub in ("severity", "binary"):
                if sub in res:
                    print(_fmt_result(f"{ds}/{sub}", res[sub]))
        else:
            print(_fmt_result(ds, res))

    # Always save results JSON
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(
        json.dumps(all_results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nResults written to {output_path}")


if __name__ == "__main__":
    main()
