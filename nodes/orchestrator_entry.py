import os

import httpx

from gen.axiom_official_axiom_agent_messages_messages_pb2 import AgentRequest
from gen.axiom_logger import AxiomLogger, AxiomSecrets


def orchestrator_entry(log: AxiomLogger, secrets: AxiomSecrets, input: AgentRequest) -> AgentRequest:
    """Entry point for the Axiom agent. Fetches the user's GitHub token via
    GET /app/github/token and attaches it to the AgentRequest before routing
    to the intent classifier.
    """
    bff_url = os.environ.get("BFF_URL", "http://axiom-bff:8083")
    axiom_api_key = secrets.get("AXIOM_API_KEY") or os.environ.get("AXIOM_API_KEY", "")

    github_token = ""
    try:
        resp = httpx.get(
            f"{bff_url}/app/github/token",
            headers={"Authorization": f"Bearer {axiom_api_key}"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            github_token = data.get("token", "")
    except Exception as e:
        log.warning(f"Failed to fetch GitHub token: {e}")

    enriched = AgentRequest()
    enriched.CopyFrom(input)
    if github_token:
        enriched.github_token = github_token

    return enriched
