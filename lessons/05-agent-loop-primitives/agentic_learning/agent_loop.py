from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable


@dataclass(frozen=True)
class AgentContext:
    """State passed into each agent step."""

    goal: str
    messages: tuple[str, ...] = ()
    artifacts: tuple[str, ...] = ()


@dataclass(frozen=True)
class AgentAction:
    """A simple action proposed by the agent."""

    kind: str
    detail: str


@dataclass(frozen=True)
class AgentOutput:
    """Final response from the agent loop."""

    summary: str
    actions: tuple[AgentAction, ...] = ()


@dataclass
class AgentLoop:
    """A tiny plan-act-reflect loop for learning purposes."""

    steps: list[str] = field(default_factory=list)

    def run(
        self,
        context: AgentContext,
        planner: Callable[[AgentContext], Iterable[AgentAction]],
        responder: Callable[[AgentContext, tuple[AgentAction, ...]], AgentOutput],
    ) -> AgentOutput:
        planned_actions = tuple(planner(context))
        self.steps.append(f"planned:{len(planned_actions)}")
        output = responder(context, planned_actions)
        self.steps.append("responded")
        return output
