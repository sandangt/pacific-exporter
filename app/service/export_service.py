from app.repository import StudentRepository, LearningResultRepository


class ExportService:
    def __init__(self, student_repository: StudentRepository, learning_result_repository: LearningResultRepository):
        self._student_repository = student_repository
        self._learning_result_repository = learning_result_repository
