from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from msme_growth_os.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Business(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "businesses"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str | None] = mapped_column(String(120))
    city: Mapped[str | None] = mapped_column(String(120))

    customers: Mapped[list["Customer"]] = relationship(back_populates="business")
    inventory_items: Mapped[list["InventoryItem"]] = relationship(back_populates="business")
    suppliers: Mapped[list["Supplier"]] = relationship(back_populates="business")
    orders: Mapped[list["Order"]] = relationship(back_populates="business")
    cash_snapshots: Mapped[list["CashSnapshot"]] = relationship(back_populates="business")
    compliance_deadlines: Mapped[list["ComplianceDeadline"]] = relationship(back_populates="business")


class Customer(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "customers"

    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32))

    business: Mapped[Business] = relationship(back_populates="customers")


class Supplier(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "suppliers"

    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    lead_time_days: Mapped[int | None]

    business: Mapped[Business] = relationship(back_populates="suppliers")
    updates: Mapped[list["SupplierUpdate"]] = relationship(back_populates="supplier")


class InventoryItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "inventory_items"

    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False)
    sku: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity_on_hand: Mapped[int] = mapped_column(default=0, nullable=False)
    reorder_level: Mapped[int | None]
    unit_cost: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    business: Mapped[Business] = relationship(back_populates="inventory_items")


class Order(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "orders"

    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False)
    customer_id: Mapped[UUID | None] = mapped_column(ForeignKey("customers.id"))
    external_reference: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="draft")
    total_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    business: Mapped[Business] = relationship(back_populates="orders")


class CashSnapshot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "cash_snapshots"

    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False)
    available_cash: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    expected_inflow: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    expected_outflow: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)

    business: Mapped[Business] = relationship(back_populates="cash_snapshots")


class ComplianceDeadline(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "compliance_deadlines"

    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending")

    business: Mapped[Business] = relationship(back_populates="compliance_deadlines")


class SupplierUpdate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "supplier_updates"

    supplier_id: Mapped[UUID] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str | None] = mapped_column(String(80))

    supplier: Mapped[Supplier] = relationship(back_populates="updates")
