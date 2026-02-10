from uuid import UUID

from sqlalchemy import String, Integer, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID 

from app.database.db import Base
from app.utils.custom_types import uuint_pk, uuid_ref, created_at, closed_at, OrderStatus

class Order(Base):
    __tablename__ = "orders"

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
        nullable=False
    )
    # TODO - OrderItems field
    closed_at: Mapped[closed_at]
    time_slot: Mapped[str] = mapped_column(String(50), nullable=False)
    
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[uuint_pk]
    order_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False
    )
    product_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped[Order] = relationship(back_populates="items")
    product: Mapped[Product] = relationship()


class Product(Base):
    __tablename__ = "products"