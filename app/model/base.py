from typing import Dict, Any

from sqlalchemy.orm import DeclarativeBase


class BaseEntity(DeclarativeBase):
    def as_dict(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def as_updatable_dict(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
            if column.name not in {'id', 'created_on', 'last_modified_on'}
        }
