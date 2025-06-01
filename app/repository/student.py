from app.model import Student
from .crud import CRUDRepository


class StudentRepository(CRUDRepository[Student]):
    _model_type = Student
