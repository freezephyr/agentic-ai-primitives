from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class GovernanceDecision:
    allowed: bool
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class GovernanceResult:
    action: str
    decision: GovernanceDecision


class GovernancePolicy:
    """Basic policy checks for agent actions."""

    def __init__(self, blocked_prefixes: Iterable[str] | None = None) -> None:
        self._blocked_prefixes = tuple(blocked_prefixes or ())

    def evaluate(self, action: str) -> GovernanceDecision:
        reasons = [
            f"blocked prefix: {prefix}"
            for prefix in self._blocked_prefixes
            if action.startswith(prefix)
        ]
        if reasons:
            return GovernanceDecision(allowed=False, reasons=tuple(reasons))
        return GovernanceDecision(allowed=True)

    def review(self, action: str) -> GovernanceResult:
        return GovernanceResult(action=action, decision=self.evaluate(action))
