import logging
import os

import httpx

from gen.axiom_official_axiom_agent_messages_messages_pb2 import AgentRequest

logger = logging.getLogger(__name__)


def handle(req: AgentRequest, context) -> AgentRequest:
    """Fetch the user's GitHub token and attach it to the request."""

    bff_url = os.environ.get("BFF_URL", "http://axiom-bff:8083")
    axiom_api_key = os.environ.get("AXIOM_API_KEY", "")

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
        logger.warning(f"Failed to fetch GitHub token: {e}")

    enriched = AgentRequest()
    enriched.CopyFrom(req)
    if github_token:
        enriched.github_token = github_token

    return enriched
