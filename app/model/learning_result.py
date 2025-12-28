import uuid

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, UUID, Float, TEXT, Integer

from app.constant import MAX_INTEGER
from .base import BaseEntity


class LearningResult(BaseEntity):
    __tablename__ = 'learning_result'
    id = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    mark = mapped_column(Float, nullable=False)
    grade = mapped_column(String, nullable=False)
    subject = mapped_column(String, nullable=False)
    subject_slug = mapped_column(String, nullable=False)
    teacher_name = mapped_column(String, nullable=False)
    comment = mapped_column(TEXT, nullable=True)
    subject_rank = mapped_column(Integer, nullable=False, default=MAX_INTEGER)

    student_id = mapped_column(ForeignKey('student.id'))
    student: Mapped['Student'] = relationship(back_populates='learning_results')
