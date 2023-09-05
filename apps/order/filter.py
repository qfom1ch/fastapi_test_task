from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from apps.order.models import Order


class OrderFilter(Filter):
    id__in: Optional[list[int]] = Field(alias="id")
    store_id__in: Optional[list[int]] = Field(alias="store_id")
    status__in: Optional[list[str]] = Field(alias="status")
    author_id__in: Optional[list[int]] = Field(alias="author_id")

    class Constants(Filter.Constants):
        model = Order

    class Config:
        allow_population_by_field_name = True
