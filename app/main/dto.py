from app.repository import StudentRepository, LearningResultRepository
from app.service import PersistService, ExportService


class ApplicationContext:
    def __init__(self, student_repository: StudentRepository,
                        learning_result_repository: LearningResultRepository,
                        persist_service: PersistService,
                        export_service: ExportService
    ):
        self.__student_repository = student_repository
        self.__learning_result_repository = learning_result_repository
        self.__persist_service = persist_service
        self.__export_service = export_service

    @property
    def student_repository(self):
        return self.__student_repository

    @property
    def learning_result_repository(self):
        return self.__learning_result_repository

    @property
    def persist_service(self):
        return self.__persist_service

    @property
    def export_service(self):
        return self.__export_service

