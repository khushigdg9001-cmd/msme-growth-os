from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class AgentInput:
    business_id: UUID
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentOutput:
    agent_name: str
    signals: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


class BusinessAgent(ABC):
    name: str

    @abstractmethod
    async def analyze(self, agent_input: AgentInput) -> AgentOutput:
        raise NotImplementedError
