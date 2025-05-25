from app.model.student import Student
from app.repository.crud import CRUDRepository


class StudentRepository(CRUDRepository[Student]):
    _model_type = Student
