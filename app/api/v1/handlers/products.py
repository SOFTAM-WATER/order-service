from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT 

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_async_session
from app.schemas.products import CreateProductRequest, ProductResponce
from app.api.v1.services.products_service import ProductService


router = APIRouter(prefix="/products")

@router.post(
    path="/create",
    status_code=HTTP_201_CREATED,
    response_model=ProductResponce
)
async def create_product(
    product: CreateProductRequest,
    session: AsyncSession = Depends(get_async_session)
):
    return await ProductService.create_new_product(session, product)