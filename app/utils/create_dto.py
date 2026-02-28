import app.grpc.generated.order_draft_pb2 as draft_pb2
from app.schemas.order_dto import CreateOrderDTO

def parse_create_order_request(request: draft_pb2.CreateOrderRequest) -> CreateOrderDTO:
    from app.schemas.order_dto import OrderItemDTO, CreateOrderDTO
    import datetime
    from uuid import UUID

    items = [
        OrderItemDTO(
            product_id=UUID(item.product_id),
            quantity=item.quantity,
            price=item.subtotal_price
        )
        for item in request.items
    ]

    delivery_date = datetime.date(
        request.delivery_date.year,
        request.delivery_date.month,
        request.delivery_date.day
    )

    slot_from = datetime.time(
        request.slot_from.hours,
        request.slot_from.minutes,
        request.slot_from.seconds,
        tzinfo=datetime.timezone.utc
    )

    slot_to = datetime.time(
        request.slot_to.hours,
        request.slot_to.minutes,
        request.slot_to.seconds,
        tzinfo=datetime.timezone.utc
    )

    return CreateOrderDTO(
        transaction_id=UUID(request.transaction_id),
        user_id=UUID(request.user_id),
        full_name=request.full_name,
        phone=request.phone,
        location=request.location,
        total_sum=request.total_sum,
        delivery_date=delivery_date,
        slot_from=slot_from,
        slot_to=slot_to,
        items=items
    )