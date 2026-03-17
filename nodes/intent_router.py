import json
import logging
import os

import anthropic

from gen.axiom_official_axiom_agent_messages_messages_pb2 import AgentRequest

logger = logging.getLogger(__name__)

VALID_INTENTS = {
    "build_package",
    "design_flow",
    "debug_package",
    "refactor_package",
    "debug_flow",
    "refactor_flow",
}

SYSTEM_PROMPT = """You are an Axiom agent intent classifier.
Classify the user's goal into exactly one of these intents:
- build_package: User wants to create a new Axiom package
- design_flow: User wants to create or design a new flow graph
- debug_package: User wants to debug a failing package/node
- refactor_package: User wants to modify or improve an existing package
- debug_flow: User wants to debug a failing flow
- refactor_flow: User wants to modify or improve an existing flow

Return JSON: {"intent": "<one of the six values above>", "confidence": 0.0-1.0}"""


def handle(req: AgentRequest, context) -> AgentRequest:
    """Classify intent and set AgentRequest.intent."""
    api_key = context.secrets.get("ANTHROPIC_API_KEY") if hasattr(context, 'secrets') else os.environ.get("ANTHROPIC_API_KEY", "")
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": req.goal}]
    )

    content = message.content[0].text
    if "```json" in content:
        start = content.index("```json") + 7
        end = content.index("```", start)
        content = content[start:end].strip()
    elif "```" in content:
        start = content.index("```") + 3
        end = content.index("```", start)
        content = content[start:end].strip()

    try:
        data = json.loads(content)
        intent = data.get("intent", "build_package")
    except json.JSONDecodeError:
        intent = "build_package"

    if intent not in VALID_INTENTS:
        intent = "build_package"

    routed = AgentRequest()
    routed.CopyFrom(req)
    routed.intent = intent

    logger.info(f"Routed intent: {intent} for goal: {req.goal[:80]}")
    return routed
