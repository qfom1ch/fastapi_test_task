from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Store


async def _get_store_by_id(id: int,
                           db_session: AsyncSession) \
        -> Union[Store, None]:
    query = select(Store).where(Store.id == id)
    res = await db_session.execute(query)
    store_row = res.fetchone()
    if store_row is not None:
        return store_row[0]
