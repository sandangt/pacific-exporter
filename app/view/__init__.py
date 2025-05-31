import os
import shutil
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.config import init_db_config, get_report_template
from app.constant import TEMP_DIR, RESULT_DIR
from app.model import BaseEntity
from app.repository import StudentRepository, LearningResultRepository
from app.service import PersistService
from app.service.export_service import ExportService
from app.view.component import MainWindow
from app.view.dto import ApplicationContext

def __init_context() -> ApplicationContext:
    # Init file system
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(RESULT_DIR, exist_ok=True)
    # Init db
    db_engine, db_session = init_db_config()
    from app.model import Student, LearningResult
    BaseEntity.metadata.create_all(bind=db_engine)
    # Init template
    report_template = get_report_template()
    # Init repositories
    student_repository = StudentRepository(db_session)
    learning_result_repository = LearningResultRepository(db_session)
    # Init services
    persist_service = PersistService(student_repository, learning_result_repository)
    export_service = ExportService(student_repository, learning_result_repository, report_template)
    return ApplicationContext(
        student_repository=student_repository,
        learning_result_repository=learning_result_repository,
        persist_service=persist_service,
        export_service=export_service,
    )

def __clean_up():
    shutil.rmtree(Path(TEMP_DIR), ignore_errors=True)

def start_app():
    app_ctx = __init_context()
    app = QApplication(sys.argv)
    widget = MainWindow(app_ctx)
    widget.resize(200, 200)
    widget.show()
    exit_code = app.exec()
    __clean_up()
    sys.exit(exit_code)
