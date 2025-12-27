import os
import shutil
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from sqlalchemy.orm import close_all_sessions

from app.config import init_db_config, init_font_config
from app.constant import TEMP_DIR, GIT_KEEP_FILE_NAME
from app.model import BaseEntity
from app.repository import StudentRepository, LearningResultRepository
from app.service import PersistService, ExportService
from app.main.view import MainWindow
from app.main.dto import ApplicationContext

def __init_context() -> ApplicationContext:
    #region Init file system
    os.makedirs(TEMP_DIR, exist_ok=True)
    #endregion
    #region Init db config
    db_engine, db_session = init_db_config()
    BaseEntity.metadata.create_all(bind=db_engine)
    #endregion
    #region Init font
    init_font_config()
    #endregion
    #region Init repositories & services
    student_repository = StudentRepository(db_session)
    learning_result_repository = LearningResultRepository(db_session)
    persist_service = PersistService(student_repository, learning_result_repository)
    export_service = ExportService(student_repository, learning_result_repository)
    #endregion
    return ApplicationContext(
        student_repository=student_repository,
        learning_result_repository=learning_result_repository,
        persist_service=persist_service,
        export_service=export_service,
        db_engine=db_engine
    )

def __close_up_db(app_ctx: ApplicationContext):
    try:
        close_all_sessions()
    except Exception:
        pass
    try:
        app_ctx.db_engine.dispose()
    except Exception:
        pass

def __clean_up_tmp_dir():
    tmp_dir = Path(TEMP_DIR)
    if not tmp_dir.exists() or not tmp_dir.is_dir():
        return
    for item in tmp_dir.iterdir():
        if item.name == GIT_KEEP_FILE_NAME:
            continue
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            item.unlink(missing_ok=True)

def start_app():
    #region Init application
    app_ctx = __init_context()
    app = QApplication(sys.argv)
    main_window = MainWindow(app_ctx)
    #endregion
    #region Start app
    main_window.show()
    exit_code = app.exec()
    #endregion
    #region Clean up
    app.quit()
    __close_up_db(app_ctx)
    __clean_up_tmp_dir()
    #endregion
    sys.exit(exit_code)

if __name__ == '__main__':
    start_app()
