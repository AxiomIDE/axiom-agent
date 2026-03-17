def test_intent_router_imports():
    import nodes.intent_router as m
    assert hasattr(m, "intent_router")


def test_valid_intents():
    from nodes.intent_router import VALID_INTENTS
    assert "build_package" in VALID_INTENTS
    assert "design_flow" in VALID_INTENTS
    assert len(VALID_INTENTS) == 6
