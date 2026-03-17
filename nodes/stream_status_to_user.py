from typing import Iterator

from gen.axiom_official_axiom_agent_messages_messages_pb2 import AgentProgress
from gen.axiom_logger import AxiomLogger, AxiomSecrets


def stream_status_to_user(log: AxiomLogger, secrets: AxiomSecrets, inputs: Iterator[AgentProgress]) -> Iterator[AgentProgress]:
    """Forwards AgentProgress frames to the user in real time, enriching the
    message with execution context for observability.
    """
    for progress in inputs:
        log.info(f"stage={progress.stage} complete={progress.complete} message={progress.message[:120]}")

        if progress.message and not progress.message.startswith("[Axiom Agent]"):
            enriched = AgentProgress()
            enriched.CopyFrom(progress)
            enriched.message = f"[Axiom Agent] {progress.message}"
            yield enriched
        else:
            yield progress
