from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.visit.services import (_create_visit, _delete_visit,
                                 _get_visit_by_id, _get_visits, _update_visit,
                                 _validations_executor_order,
                                 _validations_exist_visit,
                                 _validations_order_end_time)
from db.session import get_db

from ..customer.services import _get_customer_by_phone
from ..order.services import _get_order_by_id
from ..store.services import _get_store_by_id
from ..worker.services import _get_worker_by_id
from .filter import VisitFilter
from .schemas import ShowVisit, UpdateVisitRequest, VisitCreate

visit_router = APIRouter(
    prefix='/visits'
)


@visit_router.get("/", response_model=list[ShowVisit],
                  tags=['visits'])
async def get_visits(
        visit_filter: VisitFilter = FilterDepends(
            VisitFilter),
        db_session: AsyncSession = Depends(get_db)) \
        -> list[ShowVisit]:
    list_visits = await _get_visits(visit_filter, db_session)
    return list_visits


@visit_router.post("/", response_model=ShowVisit, tags=['visits'])
async def create_order(customer_phone: str, visit: VisitCreate,
                       db_session: AsyncSession = Depends(
                           get_db)) -> ShowVisit:
    current_customer = await _get_customer_by_phone(customer_phone, db_session)
    if current_customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    order = await _get_order_by_id(visit.order_id, db_session)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Order not found")

    executor = await _get_worker_by_id(visit.executor_id, db_session)
    if executor is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Executor with id:{visit.executor_id} does not exist",
        )

    if not await _validations_executor_order(visit.order_id, visit.executor_id,
                                             db_session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Executor must be an employee associated with the order",
        )

    if not visit.store_id == current_customer.store_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can create an visit only for your store",
        )

    if not await _validations_order_end_time(visit.order_id,
                                             db_session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order expired",
        )

    if await _validations_exist_visit(visit.order_id, db_session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Visit for this order already exists",
        )

    return await _create_visit(visit, db_session, current_customer)


@visit_router.patch("/", response_model=ShowVisit, tags=['visits'])
async def update_order(customer_phone: str,
                       visit_id: int,
                       data_to_update: UpdateVisitRequest,
                       db_session: AsyncSession = Depends(get_db)) \
        -> ShowVisit:
    current_customer = await _get_customer_by_phone(customer_phone, db_session)
    if current_customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    visit = await _get_visit_by_id(visit_id, db_session)
    if visit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visit with id {visit_id} not found"
        )

    updated_visit_params = data_to_update.dict(exclude_none=True)
    if updated_visit_params == {}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=("At least one parameter for order update "
                    "info should be provided"),
        )

    if updated_visit_params.get('executor_id', False):
        executor = await _get_worker_by_id(updated_visit_params['executor_id'],
                                           db_session)
        if executor is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Executor with id:"
                       f"{updated_visit_params['executor_id']} does not exist",
            )

    if updated_visit_params.get('store_id', False):
        store = await _get_store_by_id(updated_visit_params['store_id'],
                                       db_session)
        if store is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Store with id {updated_visit_params['store_id']} "
                       f"not found"
            )

    if updated_visit_params.get('order_id', False):
        order = await _get_order_by_id(updated_visit_params['order_id'],
                                       db_session)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {updated_visit_params['order_id']} "
                       f"not found"
            )

    author_id = visit.author_id
    if author_id != current_customer.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="You can change only your visit")
    updated_visit = await _update_visit(visit_id, updated_visit_params,
                                        db_session)
    return updated_visit


@visit_router.delete("/", status_code=status.HTTP_200_OK,
                     tags=['visits'])
async def delete_visit(
        customer_phone: str,
        visit_id: int,
        db_session: AsyncSession = Depends(get_db)) \
        -> Response:
    current_customer = await _get_customer_by_phone(customer_phone, db_session)
    if current_customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    visit = await _get_visit_by_id(visit_id, db_session)
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Visit not found")

    if visit.author_id != current_customer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can delete only your visit")
    await _delete_visit(visit_id, db_session)
    return Response(status_code=status.HTTP_200_OK)
