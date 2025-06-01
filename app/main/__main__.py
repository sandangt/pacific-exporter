import os
import shutil
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.config import init_db_config, get_report_template
from app.constant import TEMP_DIR, RESULT_DIR
from app.model import BaseEntity
from app.repository import StudentRepository, LearningResultRepository
from app.service import PersistService, ExportService
from app.main.view import MainWindow
from app.main.dto import ApplicationContext

def __init_context() -> ApplicationContext:
    #region Init file system
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(RESULT_DIR, exist_ok=True)
    #endregion
    #region Init db config
    db_engine, db_session = init_db_config()
    from app.model import Student, LearningResult
    BaseEntity.metadata.create_all(bind=db_engine)
    #endregion
    #region Init client
    report_template = get_report_template()
    #endregion
    #region Init repositories & services
    student_repository = StudentRepository(db_session)
    learning_result_repository = LearningResultRepository(db_session)
    persist_service = PersistService(student_repository, learning_result_repository)
    export_service = ExportService(student_repository, learning_result_repository, report_template)
    #endregion
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
    main_window = MainWindow(app_ctx)
    main_window.resize(200, 200)
    main_window.show()
    exit_code = app.exec()
    __clean_up()
    sys.exit(exit_code)

if __name__ == '__main__':
    start_app()
