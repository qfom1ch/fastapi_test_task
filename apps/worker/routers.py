from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.worker.schemas import ShowStore, ShowWorker
from apps.worker.services import (_get_stores_by_worker_phone,
                                  _get_worker_by_phone, _get_workers)
from db.session import get_db

from .filter import StoreFilter

worker_router = APIRouter(
    prefix='/workers',
)


@worker_router.get("/get_stores_by_worker_phone/",
                   response_model=list[ShowStore], tags=['workers'])
async def get_stores_by_phone(worker_phone: str,
                              store_filter: StoreFilter = FilterDepends(
                                  StoreFilter),
                              db_session: AsyncSession = Depends(get_db)
                              ):
    worker = await _get_worker_by_phone(worker_phone, db_session)
    if worker is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    stores = await _get_stores_by_worker_phone(worker.id,
                                               store_filter,
                                               db_session)
    return stores


@worker_router.get("/list", response_model=list[ShowWorker], tags=['workers'])
async def list_workers(db_session: AsyncSession = Depends(get_db)):
    workers = await _get_workers(db_session)
    return workers
