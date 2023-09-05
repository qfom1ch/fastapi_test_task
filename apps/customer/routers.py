from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from apps.customer.schemas import ShowCustomer
from apps.customer.services import _get_customers
from db.session import get_db

customer_router = APIRouter(
    prefix='/customers',
)


@customer_router.get("/list", response_model=list[ShowCustomer],
                     tags=['customers'])
async def list_customers(db_session: AsyncSession = Depends(get_db)):
    customers = await _get_customers(db_session)
    return customers
