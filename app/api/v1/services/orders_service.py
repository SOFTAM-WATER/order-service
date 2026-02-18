from uuid import UUID

from app.utils.service import BaseService, transaction_mode
from app.schemas.orders import CreateOrderRequest


class OrderService(BaseService):
    _repo: str = "order"

    @transaction_mode
    async def create_order(self, order: CreateOrderRequest):
        created_order = await self.uow.order.add_one_and_get_obj(**order.model_dump())
        return created_order.to_schema()