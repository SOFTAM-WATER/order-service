from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.utils.error_codes import ErrorCode
from app.grpc.clients.user_client import UserClient
from app.repositories.orders_repo import OrderRepository
from app.grpc.clients.user_client import UserClient

class OrderService():
    @staticmethod
    async def create_order(
        session: AsyncSession, 
        data,
        user_client: UserClient
    ):
        try:
            user_id = await user_client.validate_user(
                telegram_id=data.telegram_id,
                phone=data.phone,
                full_name=data.full_name
            )

            if user_id == "":
                raise AppError(
                    message="You cannot place an order for a non-existent user.",
                    code=ErrorCode.USER_NOT_FOUND,
                    status_code=HTTP_404_NOT_FOUND
                )
            
            total_sum = sum(item.price * item.quantity for item in data.items)

            order = await OrderRepository.create_order(
                session,
                order_data={
                    "user_id": user_id,
                    "full_name": data.full_name,
                    "phone": data.phone,
                    "location": data.location,
                    "delivery_date": data.delivery_date,
                    "slot_from": data.slot_from,
                    "slot_to": data.slot_to,
                    "total_sum": total_sum,  
                },
                items=[item.model_dump() for item in data.items],  
            )

            await session.commit()
            return order
            
        except IntegrityError:
            await session.rollback()
            raise AppError(
                message="An order with this data can't be created.",
                code=ErrorCode.ORDER_CREATE_FAILED,
                status_code=HTTP_409_CONFLICT
            )
        
        
