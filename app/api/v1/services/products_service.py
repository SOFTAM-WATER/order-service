from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.utils.error_codes import ErrorCode
from app.repositories.product_repo import ProductRepository

class ProductService():
    @staticmethod
    async def create_new_product(session: AsyncSession, data):
        try:
            product = await ProductRepository.create_product(
                session,
                name = data.name,
                volume = data.volume,
                price = data.price
            )

            await session.commit()
            await session.refresh(product)
            return product
        
        except IntegrityError:
            await session.rollback()
            raise AppError(
                message="Failed to create product.",
                code=ErrorCode.PRODUCT_CREATE_FAILED,
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )