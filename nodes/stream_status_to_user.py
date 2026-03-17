import logging

from gen.axiom_official_axiom_agent_messages_messages_pb2 import AgentProgress

logger = logging.getLogger(__name__)


def handle(progress: AgentProgress, context) -> AgentProgress:
    """Pipeline node: forward AgentProgress to the user in real time."""

    logger.info(f"[Agent] stage={progress.stage} complete={progress.complete} message={progress.message[:120]}")

    # In a real pipeline node the framework handles streaming; here we just pass through
    # with a formatted message for observability.
    if progress.message and not progress.message.startswith("[Axiom Agent]"):
        enriched = AgentProgress()
        enriched.CopyFrom(progress)
        enriched.message = f"[Axiom Agent] {progress.message}"
        return enriched

    return progress
