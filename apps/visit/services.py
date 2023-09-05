from datetime import datetime
from typing import Union

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.customer.models import Customer
from apps.order.models import Order
from apps.visit.filter import VisitFilter
from apps.visit.models import Visit
from apps.visit.schemas import ShowVisit, VisitCreate


async def _get_visit_by_id(id: int, db_session: AsyncSession) \
        -> Union[Order, None]:
    query = select(Visit).where(Visit.id == id)
    res = await db_session.execute(query)
    visit_row = res.fetchone()
    if visit_row is not None:
        return visit_row[0]


async def _get_visits(visit_filter: VisitFilter,
                      db_session: AsyncSession) -> list:
    query_filter = visit_filter.filter(select(Visit))
    res = await db_session.execute(query_filter)
    visits = [visit[0] for visit in res.fetchall()]
    return visits


async def _create_visit(visit: VisitCreate,
                        db_session: AsyncSession,
                        current_customer: Customer) -> ShowVisit:
    new_visit = Visit(
        creation_time=datetime.now(),
        executor_id=visit.executor_id,
        order_id=visit.order_id,
        author_id=current_customer.id,
        store_id=visit.store_id
    )
    db_session.add(new_visit)
    await db_session.flush()
    return new_visit


async def _validations_order_end_time(order_id: int,
                                      db_session: AsyncSession) -> bool:
    query = select(Order.end_time).where(Order.id == order_id)
    res = await db_session.execute(query)
    end_time_row = res.fetchone()
    return datetime.now().timestamp() < end_time_row[0].timestamp()


async def _validations_executor_order(order_id: int, executor_id: int,
                                      db_session: AsyncSession) -> bool:
    query = select(Order.executor_id).where(Order.id == order_id)
    res = await db_session.execute(query)
    executor_id_row = res.fetchone()
    return executor_id == executor_id_row[0]


async def _validations_exist_visit(order_id: int,
                                   db_session: AsyncSession) -> bool:
    stmt = select(Visit.order_id).where(Visit.order_id == order_id).exists()
    res = await db_session.execute(stmt.select())
    res_row = res.fetchone()
    return res_row[0]


async def _update_visit(visit_id: int,
                        updated_visit_params: dict,
                        db_session: AsyncSession) -> Union[Visit, None]:
    query = (
        update(Visit)
        .where(Visit.id == visit_id)
        .values(**updated_visit_params)
        .returning(Visit)
    )
    res = await db_session.execute(query)
    update_visit_row = res.fetchone()
    if update_visit_row is not None:
        return update_visit_row[0]


async def _delete_visit(visit_id: int, db_session: AsyncSession) -> None:
    query = delete(Visit).where(Visit.id == visit_id)
    await db_session.execute(query)
