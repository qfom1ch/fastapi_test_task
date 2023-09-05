from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from apps.store.models import Store


class StoreFilter(Filter):
    id__in: Optional[list[int]] = Field(alias="pk")
    name__like: Optional[str] = Field(alias="name")

    class Constants(Filter.Constants):
        model = Store

    class Config:
        allow_population_by_field_name = True
