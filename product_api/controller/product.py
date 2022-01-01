from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.sql.expression import update
from ..schemas import ProductModel, ProductPostModel
from ..model.models import Product


async def create_resource(product: ProductPostModel, session: AsyncSession):

    new_series = Product(**product.dict(exclude_unset=True))
    session.add(new_series)
    await session.commit()
    return new_series


async def get_resource(id_: UUID, session: AsyncSession):
    stm = select(Product).where(Product.id_ == id_)
    result = (await session.execute(stm)).scalars().one()
    return result
