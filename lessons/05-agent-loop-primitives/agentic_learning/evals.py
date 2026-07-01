from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    input_text: str
    expected_output: str


@dataclass(frozen=True)
class EvaluationReport:
    total: int
    passed: int
    failed_cases: tuple[str, ...]

    @property
    def score(self) -> float:
        return 0.0 if self.total == 0 else self.passed / self.total


def run_evaluation_suite(
    cases: Iterable[EvaluationCase],
    runner: Callable[[str], str],
) -> EvaluationReport:
    failed_cases: list[str] = []
    total = 0
    passed = 0

    for case in cases:
        total += 1
        actual = runner(case.input_text)
        if actual == case.expected_output:
            passed += 1
        else:
            failed_cases.append(case.name)

    return EvaluationReport(total=total, passed=passed, failed_cases=tuple(failed_cases))
