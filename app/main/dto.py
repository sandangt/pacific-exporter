from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.repository import StudentRepository, LearningResultRepository
from app.service import PersistService, ExportService


class ApplicationContext:
    def __init__(self, student_repository: StudentRepository,
                        learning_result_repository: LearningResultRepository,
                        persist_service: PersistService,
                        export_service: ExportService,
                        db_engine: Engine,
                        db_session: sessionmaker[Session]
    ):
        self.__student_repository = student_repository
        self.__learning_result_repository = learning_result_repository
        self.__persist_service = persist_service
        self.__export_service = export_service
        self.__db_engine = db_engine
        self.__db_session = db_session

    @property
    def student_repository(self) -> StudentRepository:
        return self.__student_repository

    @property
    def learning_result_repository(self) -> LearningResultRepository:
        return self.__learning_result_repository

    @property
    def persist_service(self) -> PersistService:
        return self.__persist_service

    @property
    def export_service(self) -> ExportService:
        return self.__export_service

    @property
    def db_engine(self) -> Engine:
        return self.__db_engine

    @property
    def db_session(self) -> sessionmaker[Session]:
        return self.__db_session

class SubmitEventInfo(BaseModel):
    input_dir: Optional[str]
    output_dir: Optional[str]
    ready_to_start: Optional[bool] = False
    err_msg: Optional[str] = None
