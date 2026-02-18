from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orders import Order
from app.utils.repository import SQLAlchemyRepository

class OrderRepository(SQLAlchemyRepository[Order]):
    _model = Order