from nodes.intent_router import intent_router, VALID_INTENTS


def test_intent_router_imports():
    assert callable(intent_router)

def test_valid_intents():
    
    assert "build_package" in VALID_INTENTS
    assert "design_flow" in VALID_INTENTS
    assert len(VALID_INTENTS) == 6
