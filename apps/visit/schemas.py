from datetime import datetime

from pydantic import BaseModel


class ShowVisit(BaseModel):
    id: int
    creation_time: datetime
    executor_id: int
    order_id: int
    author_id: int
    store_id: int

    class Config:
        orm_mode = True


class VisitCreate(BaseModel):
    executor_id: int
    order_id: int
    store_id: int


class UpdateVisitRequest(BaseModel):
    executor_id: int = None
    order_id: int = None
    store_id: int = None
