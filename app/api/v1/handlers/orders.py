from fastapi import APIRouter, Depends, Request
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT 

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_async_session
from app.schemas.orders import CreateOrderRequest, OrderResponce
from app.api.v1.services.orders_service import OrderService


router = APIRouter(prefix="/orders")

@router.post(
    path="/create",
    status_code=HTTP_201_CREATED,
    response_model=OrderResponce
)
async def create_product(
    request: Request,
    data: CreateOrderRequest,
    session: AsyncSession = Depends(get_async_session),
):
    return await OrderService.create_order(
        session,
        data,
        request.app.state.user_client
    )