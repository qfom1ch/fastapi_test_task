from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.customer.services import _get_customer_by_phone
from apps.order.schemas import OrderCreate, ShowOrder, UpdateOrderRequest
from apps.order.services import (_change_order_status, _create_order,
                                 _delete_order, _get_order_by_id, _get_orders,
                                 _update_order, _validations_worker_store)
from apps.worker.services import _get_worker_by_id
from db.session import get_db

from .filter import OrderFilter
from .models import Status

order_router = APIRouter(
    prefix='/orders'
)


@order_router.get("/", response_model=list[ShowOrder],
                  tags=['orders'])
async def get_orders(
        order_filter: OrderFilter = FilterDepends(
            OrderFilter),
        db_session: AsyncSession = Depends(get_db)) \
        -> list[ShowOrder]:
    list_orders = await _get_orders(order_filter, db_session)
    return list_orders


@order_router.post("/", response_model=ShowOrder, tags=['orders'])
async def create_order(customer_phone: str, order: OrderCreate,
                       db_session: AsyncSession = Depends(
                           get_db)) -> ShowOrder:
    current_customer = await _get_customer_by_phone(customer_phone, db_session)
    if current_customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    if not order.store_id == current_customer.store_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can create an order only for your store",
        )

    if await _get_worker_by_id(order.executor_id, db_session) is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Employee with id:{order.executor_id} does not exist",
        )

    if not await _validations_worker_store(order.store_id, order.executor_id,
                                           db_session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Executor must be an Employee associated with the store",
        )

    return await _create_order(order, db_session, current_customer)


@order_router.patch("/", response_model=ShowOrder, tags=['orders'])
async def update_order(customer_phone: str,
                       order_id: int,
                       data_to_update: UpdateOrderRequest,
                       db_session: AsyncSession = Depends(get_db)) \
        -> ShowOrder:
    current_customer = await _get_customer_by_phone(customer_phone, db_session)
    if current_customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    order = await _get_order_by_id(order_id, db_session)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found."
        )

    updated_order_params = data_to_update.dict(exclude_none=True)
    if updated_order_params == {}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=("At least one parameter for order update "
                    "info should be provided"),
        )

    author_id = order.author_id
    if author_id != current_customer.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="You can change only your order")
    updated_order = await _update_order(order_id, updated_order_params,
                                        db_session)
    return updated_order


@order_router.delete("/", status_code=status.HTTP_200_OK,
                     tags=['orders'])
async def delete_order(
        customer_phone: str,
        order_id: int,
        db_session: AsyncSession = Depends(get_db)) \
        -> Response:
    current_customer = await _get_customer_by_phone(customer_phone, db_session)
    if current_customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    order = await _get_order_by_id(order_id, db_session)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Order not found")

    if order.author_id != current_customer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can delete only your order")
    await _delete_order(order_id, db_session)
    return Response(status_code=status.HTTP_200_OK)


@order_router.put("/", response_model=ShowOrder, tags=['change_order_status'])
async def change_order_status(order_id: int,
                              order_status: Status,
                              db_session: AsyncSession = Depends(get_db)) \
        -> ShowOrder:
    order = await _get_order_by_id(order_id, db_session)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found."
        )

    updated_order = await _change_order_status(order_id, order_status,
                                               db_session)
    return updated_order
