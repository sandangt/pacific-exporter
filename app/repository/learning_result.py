from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.dto.list_query import PaginationParams, OrderByParams
from app.model import LearningResult


class LearningResultRepository:
    def __init__(self, db_session: sessionmaker[Session]):
        self._db_session = db_session

    def get_all(self, pagination: PaginationParams, order_by: OrderByParams) -> list[type[LearningResult]]:
        offset, size = pagination.model_dump()
        direction, order_by_property = order_by.model_dump()
        with self._db_session.begin() as session:
            items = session.query(LearningResult) \
                .order_by(direction(getattr(LearningResult, order_by_property))) \
                .offset(offset * size) \
                .limit(size) \
                .all()
            session.expunge_all()  # change objs state from persistent to detached
        return items

    def get_multiple_by_ids(self, ids: List[UUID], order_by: OrderByParams) -> list[type[LearningResult]]:
        direction, order_by_property = order_by.model_dump()
        with self._db_session.begin() as session:
            items = session.query(LearningResult) \
                .filter(LearningResult.id.in_(ids)) \
                .order_by(direction(getattr(LearningResult, order_by_property))) \
                .all()
            session.expunge_all()
        return items

    def get_one_by_id(self, id: UUID) -> Optional[LearningResult]:
        with self._db_session.begin() as session:
            item = session.get(LearningResult, id)
            session.expunge_all()
        return item

    def create(self, item: LearningResult):
        with self._db_session.begin() as session:
            try:
                session.add(item)
                session.flush()
                session.expunge(item)
            except IntegrityError as ex:
                session.rollback()
                raise ex

    def create_multiple(self, items: List[LearningResult]):
        with self._db_session.begin() as session:
            try:
                session.add_all(items)
                session.flush()
                session.expunge_all()
            except IntegrityError as ex:
                session.rollback()
                raise ex
