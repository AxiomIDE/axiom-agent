import pytest
from unittest.mock import MagicMock, patch


def test_intent_router_imports():
    import nodes.intent_router as m
    assert hasattr(m, "handle")


def test_valid_intents():
    from nodes.intent_router import VALID_INTENTS
    assert "build_package" in VALID_INTENTS
    assert "design_flow" in VALID_INTENTS
    assert len(VALID_INTENTS) == 6
