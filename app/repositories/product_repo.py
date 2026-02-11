from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Product

class ProductRepository():
    @staticmethod
    async def create_product(session: AsyncSession, **kwargs):
        product = Product(**kwargs)
        session.add(product)

        await session.flush()
        return product