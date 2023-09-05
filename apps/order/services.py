from datetime import datetime
from typing import Union

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.order.filter import OrderFilter
from apps.order.models import Order, Status

from ..customer.models import Customer
from ..store.models import Store
from ..worker.models import Worker
from .schemas import OrderCreate, ShowOrder


async def _get_order_by_id(id: int, db_session: AsyncSession) \
        -> Union[Order, None]:
    query = select(Order).where(Order.id == id)
    res = await db_session.execute(query)
    order_row = res.fetchone()
    if order_row is not None:
        return order_row[0]


async def _get_orders(order_filter: OrderFilter,
                      db_session: AsyncSession) -> list:
    query_filter = order_filter.filter(select(Order))
    res = await db_session.execute(query_filter)
    orders = [order[0] for order in res.fetchall()]
    return orders


async def _create_order(order: OrderCreate,
                        db_session: AsyncSession,
                        current_customer: Customer) -> ShowOrder:
    new_order = Order(
        creation_time=datetime.now(),
        end_time=order.end_time,
        store_id=order.store_id,
        author_id=current_customer.id,
        status=Status.started,
        executor_id=order.executor_id
    )
    db_session.add(new_order)
    await db_session.flush()
    return new_order


async def _validations_worker_store(store_id: int, worker_id: int,
                                    db_session: AsyncSession) -> bool:
    query = select(Worker.id).where(Worker.stores.any(Store.id == store_id))
    res = await db_session.execute(query)
    workers = [worker[0] for worker in res.fetchall()]
    return worker_id in workers


async def _update_order(order_id: int,
                        updated_order_params: dict,
                        db_session: AsyncSession) -> Union[Order, None]:
    query = (
        update(Order)
        .where(Order.id == order_id)
        .values(**updated_order_params)
        .returning(Order)
    )
    res = await db_session.execute(query)
    update_order_row = res.fetchone()
    if update_order_row is not None:
        return update_order_row[0]


async def _delete_order(order_id: int, db_session: AsyncSession) -> None:
    query = delete(Order).where(Order.id == order_id)
    await db_session.execute(query)


async def _change_order_status(order_id: int,
                               status: Status,
                               db_session: AsyncSession) -> Union[Order, None]:
    query = (
        update(Order)
        .where(Order.id == order_id)
        .values({'status': status})
        .returning(Order)
    )
    res = await db_session.execute(query)
    update_order_row = res.fetchone()
    if update_order_row is not None:
        return update_order_row[0]
