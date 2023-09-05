from datetime import datetime

from pydantic import BaseModel, validator

from .models import Status


class ShowOrder(BaseModel):
    id: int
    creation_time: datetime
    end_time: datetime
    store_id: int
    author_id: int
    status: Status
    executor_id: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    end_time: datetime = datetime.now()
    store_id: int
    executor_id: int

    @validator("end_time")
    def validate_title(cls, end_time: datetime):
        if end_time <= datetime.now():
            raise ValueError(
                "End time cannot be less than or equal to the current time")
        return end_time


class UpdateOrderRequest(BaseModel):
    end_time: datetime = None
    store_id: int = None
    author_id: int = None
    status: Status = None
    executor_id: int = None
