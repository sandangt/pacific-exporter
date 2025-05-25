from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm.session import sessionmaker, Session

from app.model.student import Student


class StudentRepository:
    def __init__(self, db_session: sessionmaker[Session]):
        self._db_session = db_session

    def get_all(self) -> List[Student]:
        with self._db_session.begin() as session:
            items = session.query(Student).all()
            session.expunge_all()
        return items or []

    def get_by_id(self, id: UUID) -> Optional[Student]:
        with self._db_session.begin() as session:
            item = session.get(Student, id)
            session.expunge_all()
        return item

    def get_by_slug(self, slug: str) -> Optional[Student]:
        with self._db_session.begin() as session:
            item = session.query(Student).filter_by(slug=slug).first()
            session.expunge_all()
        return item

    def upsert(self, payload: Student):
        pass

    def bulk_upsert(self, payload: List[Student]):
        pass
