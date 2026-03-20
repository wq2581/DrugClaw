#!/usr/bin/env python3
"""
self_bench/runner.py — Run all (or selected) self-benchmarks for DrugClaw.

Usage:
    # Run all benchmarks
    python -m self_bench.runner

    # Run specific benchmarks
    python -m self_bench.runner --datasets ddi_corpus drugprot

    # Specify model and sample size
    python -m self_bench.runner --model gpt-4o --n_samples 100

    # Custom output directory
    python -m self_bench.runner --output_dir ./bench_results
"""

import argparse
import json
import os
import sys
import time

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from self_bench.ddi_corpus.bench import run as run_ddi_corpus
from self_bench.drugprot.bench import run as run_drugprot
from self_bench.n2c2_2018.bench import run as run_n2c2_2018
from self_bench.phee.bench import run as run_phee
from self_bench.cadec.bench import run as run_cadec

BENCHMARKS = {
    "ddi_corpus": {
        "run": run_ddi_corpus,
        "description": "DDI Corpus 2013 — Drug-Drug Interaction type classification (advise/effect/mechanism/int)",
    },
    "drugprot": {
        "run": run_drugprot,
        "description": "DrugProt — Drug-Protein relation type classification",
    },
    "n2c2_2018": {
        "run": run_n2c2_2018,
        "description": "n2c2 2018 Track 2 — Adverse Drug Event binary classification",
    },
    "phee": {
        "run": run_phee,
        "description": "PHEE — Pharmacovigilance event type classification (adverse_event/therapeutic_outcome)",
    },
    "cadec": {
        "run": run_cadec,
        "description": "CADEC — Adverse Drug Reaction binary classification (present/absent)",
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="DrugClaw Self-Benchmark Runner — evaluate LLM accuracy on classification datasets",
    )
    parser.add_argument(
        "--datasets", nargs="*", default=None,
        choices=list(BENCHMARKS.keys()),
        help="Which benchmarks to run (default: all)",
    )
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model name (default: gpt-4o-mini)")
    parser.add_argument("--n_samples", type=int, default=50, help="Number of samples per dataset (default: 50)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for sampling (default: 42)")
    parser.add_argument("--output_dir", default=None, help="Directory to save results JSON files")
    parser.add_argument("--list", action="store_true", help="List available benchmarks and exit")
    args = parser.parse_args()

    if args.list:
        print("Available self-benchmarks:\n")
        for name, info in BENCHMARKS.items():
            print(f"  {name:<15} {info['description']}")
        return

    datasets = args.datasets or list(BENCHMARKS.keys())
    output_dir = args.output_dir or os.path.join(os.path.dirname(__file__), "results")

    print("=" * 60)
    print("DrugClaw Self-Benchmark")
    print(f"Model: {args.model}  |  Samples: {args.n_samples}  |  Seed: {args.seed}")
    print(f"Datasets: {', '.join(datasets)}")
    print(f"Output: {output_dir}")
    print("=" * 60)

    summary = {}
    for name in datasets:
        info = BENCHMARKS[name]
        print(f"\n{'─' * 60}")
        print(f"Running: {name} — {info['description']}")
        print(f"{'─' * 60}")

        t0 = time.time()
        result = info["run"](
            model=args.model,
            n_samples=args.n_samples,
            seed=args.seed,
            output_dir=output_dir,
        )
        elapsed = time.time() - t0

        if result:
            metrics = result.get("metrics", {})
            summary[name] = {
                "accuracy": metrics.get("accuracy", 0),
                "macro_f1": metrics.get("macro_f1", 0),
                "n_samples": result.get("n_samples", 0),
                "time_sec": round(elapsed, 1),
            }
        else:
            summary[name] = {"error": "no data or benchmark failed"}

    # Print final summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"{'Dataset':<15} {'Accuracy':>10} {'Macro-F1':>10} {'Samples':>8} {'Time(s)':>8}")
    print("-" * 55)
    for name, s in summary.items():
        if "error" in s:
            print(f"{name:<15} {'ERROR':>10}")
        else:
            print(f"{name:<15} {s['accuracy']:>10.3f} {s['macro_f1']:>10.3f} "
                  f"{s['n_samples']:>8d} {s['time_sec']:>8.1f}")

    # Save summary
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({"model": args.model, "benchmarks": summary}, f, indent=2)
    print(f"\nSummary saved to {summary_path}")


if __name__ == "__main__":
    main()
