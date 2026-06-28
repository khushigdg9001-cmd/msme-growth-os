from decimal import Decimal
from typing import Protocol
from uuid import UUID

from msme_growth_os.ai.agents.base import AgentInput, AgentOutput, BusinessAgent
from msme_growth_os.core.errors import NotImplementedBusinessLogicError
from msme_growth_os.domain.models import CashSnapshotRecord, ReceivableRecord


class FinanceRepository(Protocol):
    async def list_cash_snapshots(self, business_id: UUID) -> list[CashSnapshotRecord]:
        raise NotImplementedError

    async def list_outstanding_receivables(self, business_id: UUID) -> list[ReceivableRecord]:
        raise NotImplementedError


class FinanceAgent(BusinessAgent):
    name = "finance_agent"
    low_cash_threshold = Decimal("10000")
    expense_increase_ratio = Decimal("0.10")

    def __init__(self, repository: FinanceRepository | None = None) -> None:
        self._repository = repository

    async def analyze(self, agent_input: AgentInput) -> AgentOutput:
        if self._repository is None:
            raise NotImplementedBusinessLogicError(
                "Finance agent requires a finance repository before analysis."
            )

        cash_snapshots = await self._repository.list_cash_snapshots(agent_input.business_id)
        receivables = await self._repository.list_outstanding_receivables(agent_input.business_id)

        recommendations = []
        notes = []
        latest_snapshot = cash_snapshots[0] if cash_snapshots else None

        low_cash_balance = self._low_cash_balance_signal(latest_snapshot)
        if low_cash_balance is not None:
            recommendations.append(
                self._recommendation(
                    category="low_cash_balance",
                    priority="high",
                    title="Review cash reserve",
                    reason="Available cash is below the configured operating threshold.",
                    evidence=low_cash_balance,
                )
            )

        negative_cash_flow = self._negative_cash_flow_signal(latest_snapshot)
        if negative_cash_flow is not None:
            recommendations.append(
                self._recommendation(
                    category="negative_cash_flow",
                    priority="high",
                    title="Reduce short-term cash outflow",
                    reason="Expected outflow is greater than expected inflow.",
                    evidence=negative_cash_flow,
                )
            )

        increasing_expenses = self._increasing_expenses_signal(cash_snapshots)
        if increasing_expenses is not None:
            recommendations.append(
                self._recommendation(
                    category="increasing_expenses",
                    priority="medium",
                    title="Investigate rising expenses",
                    reason="Expected outflow has increased compared with the previous snapshot.",
                    evidence=increasing_expenses,
                )
            )
        elif len(cash_snapshots) < 2:
            notes.append("Increasing expense detection requires at least two cash snapshots.")

        outstanding_receivables = self._outstanding_receivables_signal(receivables)
        if outstanding_receivables is not None:
            recommendations.append(
                self._recommendation(
                    category="outstanding_receivables",
                    priority="medium",
                    title="Follow up on pending receivables",
                    reason="One or more orders appear to have unpaid receivable balances.",
                    evidence=outstanding_receivables,
                )
            )

        profitability_trend = None
        notes.append("Profitability trend is unavailable because profit history is not modeled yet.")

        return AgentOutput(
            agent_name=self.name,
            signals={
                "cash_snapshot_count": len(cash_snapshots),
                "latest_cash_snapshot": self._cash_snapshot_payload(latest_snapshot)
                if latest_snapshot is not None
                else None,
                "low_cash_balance": low_cash_balance,
                "negative_cash_flow": negative_cash_flow,
                "increasing_expenses": increasing_expenses,
                "outstanding_receivables": outstanding_receivables,
                "profitability_trend": profitability_trend,
                "recommendations": recommendations,
            },
            notes=notes,
        )

    def _low_cash_balance_signal(
        self,
        snapshot: CashSnapshotRecord | None,
    ) -> dict[str, object] | None:
        if snapshot is None or snapshot.available_cash >= self.low_cash_threshold:
            return None

        return {
            "available_cash": str(snapshot.available_cash),
            "threshold": str(self.low_cash_threshold),
            "snapshot_date": snapshot.snapshot_date.isoformat(),
        }

    def _negative_cash_flow_signal(
        self,
        snapshot: CashSnapshotRecord | None,
    ) -> dict[str, object] | None:
        if snapshot is None:
            return None

        expected_inflow = snapshot.expected_inflow or Decimal("0")
        expected_outflow = snapshot.expected_outflow or Decimal("0")
        net_cash_flow = expected_inflow - expected_outflow

        if net_cash_flow >= 0:
            return None

        return {
            "expected_inflow": str(expected_inflow),
            "expected_outflow": str(expected_outflow),
            "net_cash_flow": str(net_cash_flow),
            "snapshot_date": snapshot.snapshot_date.isoformat(),
        }

    def _increasing_expenses_signal(
        self,
        snapshots: list[CashSnapshotRecord],
    ) -> dict[str, object] | None:
        if len(snapshots) < 2:
            return None

        latest = snapshots[0]
        previous = snapshots[1]
        latest_outflow = latest.expected_outflow or Decimal("0")
        previous_outflow = previous.expected_outflow or Decimal("0")

        if previous_outflow <= 0:
            return None

        increase_ratio = (latest_outflow - previous_outflow) / previous_outflow
        if increase_ratio < self.expense_increase_ratio:
            return None

        return {
            "latest_expected_outflow": str(latest_outflow),
            "previous_expected_outflow": str(previous_outflow),
            "increase_ratio": str(increase_ratio),
            "threshold": str(self.expense_increase_ratio),
            "latest_snapshot_date": latest.snapshot_date.isoformat(),
            "previous_snapshot_date": previous.snapshot_date.isoformat(),
        }

    def _outstanding_receivables_signal(
        self,
        receivables: list[ReceivableRecord],
    ) -> dict[str, object] | None:
        if not receivables:
            return None

        total_amount = sum((receivable.total_amount for receivable in receivables), Decimal("0"))
        return {
            "count": len(receivables),
            "total_amount": str(total_amount),
            "receivables": [
                {
                    "id": str(receivable.id),
                    "status": receivable.status,
                    "total_amount": str(receivable.total_amount),
                }
                for receivable in receivables
            ],
        }

    def _cash_snapshot_payload(self, snapshot: CashSnapshotRecord) -> dict[str, object]:
        return {
            "id": str(snapshot.id),
            "available_cash": str(snapshot.available_cash),
            "expected_inflow": str(snapshot.expected_inflow)
            if snapshot.expected_inflow is not None
            else None,
            "expected_outflow": str(snapshot.expected_outflow)
            if snapshot.expected_outflow is not None
            else None,
            "snapshot_date": snapshot.snapshot_date.isoformat(),
        }

    def _recommendation(
        self,
        category: str,
        priority: str,
        title: str,
        reason: str,
        evidence: dict[str, object],
    ) -> dict[str, object]:
        return {
            "category": category,
            "priority": priority,
            "title": title,
            "reason": reason,
            "evidence": evidence,
        }
