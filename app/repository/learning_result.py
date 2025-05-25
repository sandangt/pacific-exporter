from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import sessionmaker, Session

from app.model import LearningResult


class LearningResultRepository:
    def __init__(self, db_session: sessionmaker[Session]):
        self._db_session = db_session

    def get_all(self) -> List[LearningResult]:
        with self._db_session.begin() as session:
            items = session.query(LearningResult).all()
            session.expunge_all()
        return items or []

    def get_by_id(self, id: UUID) -> Optional[LearningResult]:
        with self._db_session.begin() as session:
            item = session.get(LearningResult, id)
            session.expunge_all()
        return item

    def create(self, payload: LearningResult):
        with self._db_session.begin() as session:
            try:
                session.add(payload)
                session.flush()
                session.expunge(payload)
            except IntegrityError as ex:
                session.rollback()
                raise ex

    def create_all(self, payload: List[LearningResult]):
        with self._db_session.begin() as session:
            try:
                session.add_all(payload)
                session.flush()
                session.expunge_all()
            except IntegrityError as ex:
                session.rollback()
                raise ex
