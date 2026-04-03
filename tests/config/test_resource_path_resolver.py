from __future__ import annotations

from pathlib import Path

from drugclaw.resource_path_resolver import (
    get_repo_root,
    resolve_path_value,
    resolve_skill_config_paths,
)


def test_resolve_path_value_uses_repo_root_for_relative_paths() -> None:
    repo_root = get_repo_root()

    resolved = resolve_path_value("resources_metadata/dti/TarKG/tarkg.tsv")

    assert resolved == repo_root / "resources_metadata" / "dti" / "TarKG" / "tarkg.tsv"


def test_resolve_skill_config_paths_uses_repo_local_defaults_for_known_skills() -> None:
    repo_root = get_repo_root()

    resolved = resolve_skill_config_paths("DRKG", {})

    assert resolved["drkg_tsv"] == str(
        repo_root / "resources_metadata" / "drug_repurposing" / "DRKG" / "drkg.tsv"
    )


def test_resolve_skill_config_paths_preserves_explicit_absolute_paths(tmp_path: Path) -> None:
    explicit = tmp_path / "custom.csv"

    resolved = resolve_skill_config_paths("RepoDB", {"csv_path": str(explicit)})

    assert resolved["csv_path"] == str(explicit)
