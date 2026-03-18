from drugclaw import cli


def test_run_query_does_not_print_answer_twice(monkeypatch, capsys) -> None:
    class FakeSystem:
        def __init__(self, config):
            self.config = config

        def query(self, query, thinking_mode, resource_filter):
            print("only-once")
            return {"answer": "only-once", "success": True}

    monkeypatch.setattr(cli, "DrugClawSystem", FakeSystem)
    monkeypatch.setattr(cli, "Config", lambda key_file: object())

    exit_code = cli._run_query(
        query="demo",
        thinking_mode="simple",
        key_file="navigator_api_keys.json",
        resource_filter=["DailyMed"],
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.count("only-once") == 1


def test_run_query_can_print_structured_evidence_summary(monkeypatch, capsys) -> None:
    class FakeSystem:
        def __init__(self, config):
            self.config = config

        def query(self, query, thinking_mode, resource_filter):
            print("answer-once")
            return {
                "answer": "answer-once",
                "success": True,
                "final_answer_structured": {
                    "summary_confidence": 0.75,
                    "key_claims": [
                        {
                            "claim": "Imatinib targets ABL1.",
                            "confidence": 0.75,
                            "evidence_ids": ["E1", "E2"],
                        }
                    ],
                    "warnings": ["Evidence conflict detected for claim: Imatinib targets ABL1."],
                    "limitations": ["Claim relies on a single source: Imatinib targets ABL1."],
                },
            }

    monkeypatch.setattr(cli, "DrugClawSystem", FakeSystem)
    monkeypatch.setattr(cli, "Config", lambda key_file: object())

    exit_code = cli._run_query(
        query="demo",
        thinking_mode="simple",
        key_file="navigator_api_keys.json",
        resource_filter=["BindingDB"],
        show_evidence=True,
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "summary_confidence=0.75" in captured.out
    assert "Imatinib targets ABL1." in captured.out
