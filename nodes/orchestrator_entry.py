from gen.axiom_official_axiom_agent_messages_messages_pb2 import AgentRequest
from gen.axiom_logger import AxiomLogger, AxiomSecrets


def orchestrator_entry(log: AxiomLogger, secrets: AxiomSecrets, input: AgentRequest) -> AgentRequest:
    """Entry point for the Axiom agent. Validates the prompt is non-empty."""
    if not input.prompt or not input.prompt.strip():
        raise ValueError("AgentRequest.prompt must not be empty")
    log.info(f"Agent started — prompt: {input.prompt[:120]}")
    return input
