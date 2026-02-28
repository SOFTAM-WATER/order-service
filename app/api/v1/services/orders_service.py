from uuid import UUID

from uuid import UUID, uuid4

from app.models.orders import OrderItem, OrderStatus
from app.utils.service import BaseService, transaction_mode
from app.schemas.order_dto import CreateOrderDTO


class OrderService(BaseService):
    _repo: str = "order"

    @transaction_mode
    async def create_order_and_get_id(self, order: CreateOrderDTO) -> UUID:
        order_id = uuid4()

        await self.uow.order.add_one_and_get_obj(
            id=order_id,
            transaction_id=order.transaction_id,
            user_id=order.user_id,
            full_name=order.full_name,
            phone=order.phone,
            location=order.location,
            total_sum=order.total_sum,
            delivery_date=order.delivery_date,
            slot_from=order.slot_from,
            slot_to=order.slot_to,
            status=OrderStatus.PENDING
        )

        for item in order.items:
            subtotal = item.quantity * item.price
            await self.uow.session_add(OrderItem(
                order_id=order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
                subtotal_price=subtotal
            ))
        
        return order_id