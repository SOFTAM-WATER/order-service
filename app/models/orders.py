import datetime

from sqlalchemy import String, Integer, Enum as SqlEnum, ForeignKey, CheckConstraint, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.utils.custom_types import uuint_pk, uuid_ref, created_at, closed_at, OrderStatus
from app.models.products import Product


class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint("total_sum >= 0", name="ck_orders_total_sum_gte_0"),
        CheckConstraint("slot_to > slot_from", name="ck_orders_slot_valid_range")
    )

    id: Mapped[uuint_pk]
    user_id: Mapped[uuid_ref]
    full_name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(255))
    total_sum: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[created_at]

    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(OrderStatus), 
        default=OrderStatus.PENDING, 
        nullable=False,
        index=True
    )

    closed_at: Mapped[closed_at]

    delivery_date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    slot_from: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    slot_to: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_order_items_price_gte_0"),
        CheckConstraint("quantity > 0", name="ck_order_items_quantity_gt_0")
    )

    id: Mapped[uuint_pk]

    order_id: Mapped[uuid_ref] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    product_id: Mapped[uuid_ref] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped[Order] = relationship(back_populates="items")
    product: Mapped[Product] = relationship()
