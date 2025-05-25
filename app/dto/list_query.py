
import json
from typing import Optional, Tuple, Any, List
from uuid import UUID

from pydantic import BaseModel, model_serializer
from pydantic.alias_generators import to_snake
from sqlalchemy import asc, desc

class PaginationParams(BaseModel):
    __DEFAULT_PAGE_SIZE = 10
    offset: int
    size: int

    @model_serializer
    def serialize(self) -> Tuple[int, int]:
        return self.offset or 0, self.size or self.DEFAULT_PAGE_SIZE


class OrderByParams(BaseModel):
    order: Optional[str]

    @model_serializer
    def serialize(self) -> Tuple[Any, str]:
        order_direction, order_by_property = asc, self.order
        if self.order.startswith('-'):
            order_direction = desc
            order_by_property = self.order[1:]
        return order_direction, to_snake(order_by_property)


class GetMultipleIdsParams(BaseModel):
    ids: Optional[str]

    @model_serializer
    def serialize(self) -> List[UUID | int]:
        return json.loads(self.ids)
