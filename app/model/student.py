import uuid
from typing import List

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.sqltypes import String, UUID, Integer

from .base import BaseEntity


class Student(BaseEntity):
    __tablename__ = 'student'
    id = mapped_column(UUID, primary_key=True, default=uuid.uuid1)
    slug = mapped_column(String, unique=True, nullable=False)
    class_code = mapped_column(String, nullable=False)
    name = mapped_column(String, nullable=False)
    semester_title = mapped_column(String, nullable=True)
    no_in_class = mapped_column(Integer, nullable=True)

    learning_results: Mapped[List['LearningResult']] = relationship(back_populates='student', lazy='joined', order_by='LearningResult.subject_rank.asc()')
