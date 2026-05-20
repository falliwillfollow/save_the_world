from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


Severity = Literal["info", "warning", "error"]
GateStatus = Literal["pass", "warn", "fail"]


SURVIVAL_CRITICAL_MDL = {
    "water",
    "food",
    "shelter",
    "sanitation",
    "energy",
    "health",
}


@dataclass(frozen=True)
class ValidationIssue:
    severity: Severity
    message: str
    path: str = "$"


@dataclass
class ValidationReport:
    path: str
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)


@dataclass(frozen=True)
class MissingDependency:
    pattern_id: str
    dependency_id: str
    dependency_kind: str
    critical: bool
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "dependency_id": self.dependency_id,
            "dependency_kind": self.dependency_kind,
            "critical": self.critical,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class GateResult:
    gate: str
    status: GateStatus
    evidence: list[str]
    remediation: list[str]
    survival_critical: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate,
            "status": self.status,
            "survival_critical": self.survival_critical,
            "evidence": self.evidence,
            "remediation": self.remediation,
        }

