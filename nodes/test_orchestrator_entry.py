def test_orchestrator_entry_imports():
    import nodes.orchestrator_entry as m
    assert hasattr(m, "handle")
