from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_root_does_not_expose_legacy_helper_files() -> None:
    assert not (ROOT / "example_usage.py").exists()
    assert not (ROOT / "run_minimal.py").exists()
    assert not (ROOT / "get_reason_detail.py").exists()
    assert not (ROOT / "query_teamplate.py").exists()


def test_readmes_do_not_contain_machine_specific_cd() -> None:
    assert "cd /data/boom/Agent/DrugClaw" not in (
        ROOT / "README.md"
    ).read_text(encoding="utf-8")
    assert "cd /data/boom/Agent/DrugClaw" not in (
        ROOT / "README_CN.md"
    ).read_text(encoding="utf-8")
