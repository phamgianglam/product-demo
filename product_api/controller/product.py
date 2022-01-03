from re import search
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_, or_
from product_api.utility.paging import PagingParam, count_query, paging_query
from product_api.utility.searcher import SearcherParams, Seracher
from ..schemas import ProductModel, ProductPostModel
from ..model.models import Product
from ..helper import update_filter_record


async def create_resource(product: ProductPostModel, session: AsyncSession):

    new_series = Product(**product.dict(exclude_unset=True))
    session.add(new_series)
    await session.commit()
    return new_series


async def get_resource(id_: UUID, session: AsyncSession):
    stm = select(Product).where(Product.id_ == id_)
    result = (await session.execute(stm)).scalars().one()
    return result


async def list_resource(price: str, search_param: SearcherParams, paging_param: PagingParam, session: AsyncSession):
    stmt = select(Product)

    if price:
        price = price.split("-")

        if len(price) != 2:
            raise ValueError("input should follow pattern minValue-maxValue")

        for i in range(len(price)):
            price[i] = int(price[i].strip())

        if price[0] > price[1]:
            raise ValueError("min value should not be greater than max")

        stmt = stmt.filter(
            and_(Product.price >= price[0], Product.price <= price[1]))

    searcher = Seracher(search_param, Product, ProductModel, "name")
    stmt = await searcher.apply_searcher(stmt)
    count_stmt = await count_query(stmt)
    paging_stmt = await paging_query(stmt, paging_param.page, paging_param.size)

    result = (await session.execute(paging_stmt)).scalars().all()
    count = (await session.execute(count_stmt)).scalars().one()
    serch_term, sort_term = await searcher.collect_term()
    
    await update_filter_record(serch_term, sort_term, price)
   
    return result, count
