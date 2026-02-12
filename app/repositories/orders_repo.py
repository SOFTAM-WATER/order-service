from typing import Mapping, Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orders import Order, OrderItem

class OrderRepository():
    @staticmethod
    async def create_order(
        session: AsyncSession, 
        order_data: Mapping[str, Any],
        items: Sequence[Mapping[str, Any]]
    ):
        order = Order(**order_data)

        order.items = [
            OrderItem(
                product_id=item["product_id"],
                quantity=item.get("quantity", 1),
                price=item["price"]
            )
            for item in items
        ]

        session.add(order)
        await session.flush()
        return order