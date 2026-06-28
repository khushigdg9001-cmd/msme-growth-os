from dataclasses import dataclass, field


@dataclass(frozen=True)
class RecommendationDraft:
    title: str
    rationale: str | None = None
    priority: str | None = None
    evidence: dict = field(default_factory=dict)
