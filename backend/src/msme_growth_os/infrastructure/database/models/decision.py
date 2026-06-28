from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from msme_growth_os.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Recommendation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "recommendations"

    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="draft")
    priority: Mapped[str | None] = mapped_column(String(40))
    rationale: Mapped[str | None] = mapped_column(Text)
    evidence: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class WorkflowAction(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_actions"

    recommendation_id: Mapped[UUID] = mapped_column(ForeignKey("recommendations.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending_approval")
    payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
