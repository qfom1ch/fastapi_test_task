from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.store.models import Store
from apps.worker.filter import StoreFilter
from apps.worker.models import Worker


async def _get_worker_by_phone(worker_phone: str, db_session: AsyncSession) \
        -> Union[Worker, None]:
    query = select(Worker).where(Worker.phone == worker_phone)
    res = await db_session.execute(query)
    worker_row = res.fetchone()
    if worker_row is not None:
        return worker_row[0]


async def _get_worker_by_id(id: int, db_session: AsyncSession) \
        -> Union[Worker, None]:
    query = select(Worker).where(Worker.id == id)
    res = await db_session.execute(query)
    worker_row = res.fetchone()
    if worker_row is not None:
        return worker_row[0]


async def _get_stores_by_worker_phone(worker_id: int,
                                      store_filter: StoreFilter,
                                      db_session: AsyncSession) -> list:
    query_filter = store_filter.filter(
        select(Store).where(Store.workers.any(Worker.id == worker_id)))
    res = await db_session.execute(query_filter)
    stores = [store[0] for store in res.fetchall()]
    return stores


async def _get_workers(db_session: AsyncSession) -> list:
    query = select(Worker)
    res = await db_session.execute(query)
    list_workers = [user[0] for user in res.fetchall()]
    return list_workers
