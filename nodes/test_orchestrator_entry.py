from nodes.orchestrator_entry import orchestrator_entry


def test_orchestrator_entry_imports():
    assert callable(orchestrator_entry)
