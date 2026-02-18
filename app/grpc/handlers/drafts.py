from typing import Type
import grpc, datetime

from uuid import UUID, uuid4

from app.models.orders import OrderItem
from app.utils.unit_of_work import UnitOfWork
import app.grpc.generated.order_draft_pb2 as draft_pb2
import app.grpc.generated.order_draft_pb2_grpc as draft_pb2_grpc


class OrderServiceGrpc(draft_pb2_grpc.OrderServiceServicer):
    def __init__(self, uow_factory: Type[UnitOfWork]):
        self._uow_factory = uow_factory

    async def CreateOrderFromDraft(self, request: draft_pb2.CreateOrderRequest, context: grpc.aio.ServicerContext):
        if not request.user_id:
            return context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "user_id is required"
            )
        
        if request.total_sum < 0:
            return context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "total_sum must be non-negative"
            )
        
        d = request.delivery_date
        delivery_date = datetime.date(d.year, d.month, d.day)

        sf = request.slot_from
        slot_from = datetime.time(sf.hours, sf.minutes, sf.seconds)
        
        st = request.slot_to
        slot_to = datetime.time(st.hours, st.minutes, st.seconds)
        
        try:
            async with self._uow_factory() as uow:
                order_id = uuid4()
                
                await uow.order.add_one_and_get_obj(
                    id=order_id,
                    transaction_id=UUID(request.transaction_id), 
                    user_id=UUID(request.user_id),
                    full_name=request.full_name,
                    phone=request.phone,
                    location=request.location,
                    total_sum=request.total_sum,
                    delivery_date=delivery_date,
                    slot_from=slot_from,
                    slot_to=slot_to,
                    status="CREATED"
                )

                for item in request.items:
                    await uow.session_add(OrderItem(
                        order_id=order_id,
                        product_id=UUID(item.product_id),
                        quantity=item.quantity,
                        price_at_order=item.subtotal_price / item.quantity 
                    ))

                return draft_pb2.OrderResponse(
                    order_id=str(order_id),
                    status="SUCCESS"
                )
            
        except Exception as e:
            return await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")