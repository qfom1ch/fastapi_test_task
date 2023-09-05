from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from apps.visit.models import Visit


class VisitFilter(Filter):
    id__in: Optional[list[int]] = Field(alias="id")
    executor_id__in: Optional[list[int]] = Field(alias="executor_id")
    order_id__in: Optional[list[int]] = Field(alias="order_id")
    author_id__in: Optional[list[int]] = Field(alias="author_id")
    store_id__in: Optional[list[int]] = Field(alias="store_id")

    class Constants(Filter.Constants):
        model = Visit

    class Config:
        allow_population_by_field_name = True
