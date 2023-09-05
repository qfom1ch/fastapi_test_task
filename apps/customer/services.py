from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Customer


async def _get_customer_by_phone(phone: str,
                                 db_session: AsyncSession) \
        -> Union[Customer, None]:
    query = select(Customer).where(Customer.phone == phone)
    res = await db_session.execute(query)
    customer_row = res.fetchone()
    if customer_row is not None:
        return customer_row[0]


async def _get_customers(db_session: AsyncSession) -> list:
    query = select(Customer)
    res = await db_session.execute(query)
    list_customers = [user[0] for user in res.fetchall()]
    return list_customers
