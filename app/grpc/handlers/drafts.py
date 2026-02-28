import grpc
import logging

from app.api.v1.services.orders_service import OrderService
import app.grpc.generated.order_draft_pb2 as draft_pb2
import app.grpc.generated.order_draft_pb2_grpc as draft_pb2_grpc
from app.utils.create_dto import parse_create_order_request

logger = logging.getLogger("order_service_grpc")

class OrderServiceGrpc(draft_pb2_grpc.OrderServiceServicer):
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    async def CreateOrderFromDraft(self, request, context):
        if not request.user_id:
            return await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "user_id is required")
        if request.total_sum < 0:
            return await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "total_sum must be non-negative")

        try:
            dto = parse_create_order_request(request)

            for item in dto.items:
                if item.quantity <= 0:
                    return await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "quantity must be > 0")

            async with self._uow_factory() as uow:
                service = OrderService(uow)
                order_id = await service.create_order_and_get_id(dto)

            return draft_pb2.OrderResponse(order_id=str(order_id), status="SUCCESS")

        except Exception as e:
            logger.exception("Error creating order from draft")
            return await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")