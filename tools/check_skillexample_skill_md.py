#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_EXAMPLES_DIR = ROOT / "skillexamples"
TOOLS_DIR = ROOT / "tools"


def find_skill_md(py_path: Path) -> Path | None:
    candidates = [
        py_path.with_name(f"{py_path.stem}_SKILL.md"),
        py_path.with_name(f"{py_path.stem}SKILL.md"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def frontmatter_ok(md_path: Path) -> tuple[bool, list[str]]:
    text = md_path.read_text(encoding="utf-8")
    problems: list[str] = []
    if not text.startswith("---\n"):
        problems.append("missing opening frontmatter fence")
        return False, problems
    parts = text.split("---", 2)
    if len(parts) < 3:
        problems.append("malformed frontmatter")
        return False, problems
    frontmatter = parts[1]
    if not re.search(r"(?m)^name:\s*\S", frontmatter):
        problems.append("missing name field")
    if not re.search(r"(?m)^description:\s*(>|.+)", frontmatter):
        problems.append("missing description field")
    return len(problems) == 0, problems


def collect_runtime_test_numbers() -> set[str]:
    numbers: set[str] = set()
    for path in TOOLS_DIR.glob("test_skill_*.py"):
        match = re.search(r"test_skill_(\d+)_", path.name)
        if match:
            numbers.add(match.group(1))
    for path in TOOLS_DIR.glob("test_skills_*.py"):
        for num in re.findall(r"(\d+)", path.stem):
            if len(num) == 2:
                numbers.add(num)
    for path in TOOLS_DIR.glob("*_smoke_test.py"):
        match = re.match(r"(\d+)_", path.name)
        if match:
            numbers.add(match.group(1))
    return numbers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit skillexamples/*.py against *_SKILL.md coverage and test coverage.",
    )
    parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Print only examples missing *_SKILL.md.",
    )
    args = parser.parse_args()

    py_files = sorted(SKILL_EXAMPLES_DIR.glob("*.py"))
    test_numbers = collect_runtime_test_numbers()

    missing: list[str] = []
    malformed: list[str] = []
    naming_nonstandard: list[str] = []
    tested_without_md: list[str] = []

    for py_path in py_files:
        number = py_path.name.split("_", 1)[0]
        md_path = find_skill_md(py_path)
        if not md_path:
            missing.append(py_path.name)
            if number in test_numbers:
                tested_without_md.append(py_path.name)
            continue

        if md_path.name == f"{py_path.stem}SKILL.md":
            naming_nonstandard.append(md_path.name)

        ok, problems = frontmatter_ok(md_path)
        if not ok:
            malformed.append(f"{md_path.name}: {', '.join(problems)}")

    if args.only_missing:
        for item in missing:
            print(item)
        return 1 if missing else 0

    print(f"examples_total={len(py_files)}")
    print(f"skill_md_missing={len(missing)}")
    print(f"skill_md_malformed={len(malformed)}")
    print(f"skill_md_nonstandard_name={len(naming_nonstandard)}")
    print(f"runtime_tests_detected={len(test_numbers)}")
    print(f"tested_without_skill_md={len(tested_without_md)}")
    print("")

    if missing:
        print("[missing]")
        for item in missing:
            print(item)
        print("")

    if malformed:
        print("[malformed]")
        for item in malformed:
            print(item)
        print("")

    if naming_nonstandard:
        print("[nonstandard_name]")
        for item in naming_nonstandard:
            print(item)
        print("")

    if tested_without_md:
        print("[tested_without_skill_md]")
        for item in tested_without_md:
            print(item)

    return 1 if missing or malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
