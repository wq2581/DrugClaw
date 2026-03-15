#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_EXAMPLES_DIR = ROOT / "skillexamples"
TOOLS_DIR = ROOT / "tools"


def existing_skill_md_path(py_path: Path) -> Path | None:
    candidates = [
        py_path.with_name(f"{py_path.stem}_SKILL.md"),
        py_path.with_name(f"{py_path.stem}SKILL.md"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def target_skill_md_path(py_path: Path) -> Path:
    return py_path.with_name(f"{py_path.stem}_SKILL.md")


def normalize_name(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    if len(cleaned) > 56:
        cleaned = "-".join(cleaned.split("-")[:6]).strip("-")
    return cleaned or "drug-resource-query"


def to_title(stem: str) -> str:
    base = re.sub(r"^\d+_", "", stem)
    return base.replace("_", " ")


def load_module_info(py_path: Path) -> tuple[str, list[str], bool]:
    source = py_path.read_text(encoding="utf-8")
    module = ast.parse(source)
    docstring = ast.get_docstring(module) or ""
    functions = [
        node.name for node in module.body
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    ]
    has_main = 'if __name__ == "__main__"' in source
    return docstring, functions, has_main


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def extract_urls(text: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for match in re.findall(r"https?://[^\s)>\"']+", text):
        if match not in seen:
            seen.add(match)
            urls.append(match)
    return urls


def extract_field(docstring: str, label: str) -> str:
    pattern = rf"{re.escape(label)}:\s*(.+?)(?=\s+[A-Za-z][A-Za-z /-]*:|$)"
    for line in docstring.splitlines():
        match = re.search(pattern, line.strip(), flags=re.IGNORECASE)
        if match:
            return match.group(1).strip().strip("|").strip()
    return ""


def build_description(title: str, category: str, subcategory: str) -> str:
    fragments = [f"Query or inspect the {title} resource"]
    if category:
        fragments.append(f"for {category.lower()} tasks")
    if subcategory:
        fragments.append(f"with emphasis on {subcategory.lower()}")
    fragments.append(
        "Use whenever Codex needs the calling pattern, downloadable entrypoint, "
        "or example query flow from this skill example script."
    )
    return " ".join(fragments)


def find_validation_script(py_path: Path) -> Path | None:
    number = py_path.stem.split("_", 1)[0]
    direct = sorted(TOOLS_DIR.glob(f"test_skill_{number}_*.py"))
    if direct:
        return direct[0]
    smoke = sorted(TOOLS_DIR.glob(f"{number}_*_smoke_test.py"))
    if smoke:
        return smoke[0]
    grouped = sorted(TOOLS_DIR.glob("test_skills_*.py"))
    for candidate in grouped:
        range_match = re.search(r"test_skills_(\d+)_(\d+)$", candidate.stem)
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            if start <= int(number) <= end:
                return candidate
        stem_numbers = re.findall(r"(\d+)", candidate.stem)
        if number in stem_numbers:
            return candidate
    return None


def extract_list_literal(source: str, var_name: str) -> list[str]:
    pattern = rf"{re.escape(var_name)}\s*=\s*\[(.*?)\]"
    match = re.search(pattern, source, flags=re.DOTALL)
    if not match:
        return []
    try:
        node = ast.parse(f"{var_name} = [{match.group(1)}]")
    except SyntaxError:
        return []
    assign = node.body[0]
    if not isinstance(assign, ast.Assign) or not isinstance(assign.value, ast.List):
        return []
    values: list[str] = []
    for elt in assign.value.elts:
        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
            values.append(elt.value)
    return values


def extract_import_lines(source: str) -> list[str]:
    imports: list[str] = []
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("from skills.") or stripped.startswith("import skills."):
            imports.append(stripped)
    return imports[:3]


def validation_block(py_path: Path) -> tuple[list[str], list[str]]:
    test_path = find_validation_script(py_path)
    if not test_path:
        return (
            ["- No dedicated `tools/` validation script is present for this example yet."],
            [
                "- Before claiming this resource is stable, add a smoke test under `tools/` that exercises the paired runtime skill."
            ],
        )

    source = test_path.read_text(encoding="utf-8")
    checks = extract_list_literal(source, "checks")
    imports = extract_import_lines(source)
    lines = [
        f"- Validation script: `{test_path.relative_to(ROOT)}`",
        f"- Run: `python {test_path.relative_to(ROOT).as_posix()}`",
    ]
    if imports:
        for item in imports:
            lines.append(f"- Runtime import: `{item}`")

    note_lines: list[str] = []
    if checks:
        note_lines.append("- The validation script currently checks:")
        for item in checks[:8]:
            note_lines.append(f"- {item}")
    else:
        note_lines.append("- Inspect the validation script directly for its current assertions and sample entities.")
    return lines, note_lines


def build_markdown(py_path: Path) -> str:
    docstring, functions, has_main = load_module_info(py_path)
    title = first_nonempty_line(docstring) or to_title(py_path.stem)
    category = extract_field(docstring, "Category")
    access_type = extract_field(docstring, "Type")
    subcategory = extract_field(docstring, "Subcategory")
    link = extract_field(docstring, "Link")
    paper = extract_field(docstring, "Paper")
    urls = extract_urls(docstring)
    name = normalize_name(f"{to_title(py_path.stem)} query")
    description = build_description(title, category, subcategory)
    validation_lines, validation_notes = validation_block(py_path)

    usage_lines: list[str] = []
    if functions:
        for fn in functions[:8]:
            usage_lines.append(f"| `{fn}()` | See `{py_path.name}` for exact input/output behavior. |")
    else:
        usage_lines.append(f"| module script | Read `{py_path.name}` and follow the top-level flow. |")

    notes: list[str] = []
    if has_main:
        notes.append(
            f"- Review `if __name__ == \"__main__\"` in `{py_path.name}` first when generating runnable query code."
        )
    else:
        notes.append(f"- `{py_path.name}` does not expose a runnable `__main__` block; call exported functions directly.")
    if link:
        notes.append(f"- Primary link from the example: <{link}>")
    if paper:
        notes.append(f"- Reference paper from the example: <{paper}>")

    source_lines = []
    for url in ([link, paper] + urls):
        if url and url not in source_lines:
            source_lines.append(url)
    if not source_lines:
        source_lines.append("Inspect the module docstring in the paired `.py` file for upstream details.")

    lines = [
        "---",
        f"name: {name}",
        "description: >",
        f"  {description}",
        "---",
        "",
        f"# {title if not title.lower().endswith(' skill') else title}",
        "",
        "Use this file as the compact operator guide for the paired `skillexamples` script.",
        "Prefer reading the Python example itself for exact request parameters, field names,",
        "and response handling.",
        "",
        "## Paired Example",
        "",
        f"- Script: `{py_path.name}`",
    ]
    if category:
        lines.append(f"- Category: `{category}`")
    if access_type:
        lines.append(f"- Type: `{access_type}`")
    if subcategory:
        lines.append(f"- Subcategory: `{subcategory}`")
    lines += [
        "",
        "## API Surface",
        "",
        "| Function | Purpose |",
        "|---|---|",
        *usage_lines,
        "",
        "## Usage",
        "",
        f"Read `{py_path.name}` and copy its call pattern when writing Code Agent query code.",
        "Keep network timeouts short and preserve the script's native access method",
        "(REST, direct download, local file scan, or HTML scraping).",
        "",
        "## Validation",
        "",
        *validation_lines,
        "",
        "## Notes",
        "",
        *notes,
        *validation_notes,
        "",
        "## Data Source",
        "",
    ]
    for source in source_lines:
        if source.startswith("http"):
            lines.append(f"- <{source}>")
        else:
            lines.append(f"- {source}")
    lines.append("")
    return "\n".join(lines)


def resolve_targets(requested: list[str]) -> list[Path]:
    all_py = sorted(SKILL_EXAMPLES_DIR.glob("*.py"))
    if not requested:
        return all_py

    resolved: list[Path] = []
    for item in requested:
        candidate = SKILL_EXAMPLES_DIR / item
        if candidate.exists():
            resolved.append(candidate)
            continue
        matches = sorted(SKILL_EXAMPLES_DIR.glob(f"{item}*.py"))
        if matches:
            resolved.extend(matches)
            continue
        raise SystemExit(f"Unrecognized target: {item}")
    return sorted(set(resolved))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or update *_SKILL.md files for skillexamples.",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Specific example filenames or numeric prefixes, e.g. 56 or 56_RxList.py",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing *_SKILL.md files instead of only generating missing ones.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing files.",
    )
    args = parser.parse_args()

    changed = 0
    skipped = 0
    targets = resolve_targets(args.targets)

    for py_path in targets:
        existing = existing_skill_md_path(py_path)
        output_path = target_skill_md_path(py_path)
        if existing and not args.overwrite:
            skipped += 1
            print(f"SKIP {py_path.name} -> {existing.name}")
            continue

        action = "UPDATE" if existing else "CREATE"
        print(f"{action} {py_path.name} -> {output_path.name}")
        if args.dry_run:
            continue

        output_path.write_text(build_markdown(py_path), encoding="utf-8")
        changed += 1

    print(
        f"done: changed={changed} skipped={skipped} total_targets={len(targets)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
