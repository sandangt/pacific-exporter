import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Any

from app.config import init_db_config, get_report_template
from app.constant import XLSX_EXTENSION, DEV_NULL_DIR, TEMP_DIR, RESULT_DIR
from app.model import BaseEntity
from app.repository import StudentRepository, LearningResultRepository
from app.service import PersistService
from app.service.export_service import ExportService


def init_context() -> Dict[str, Any]:
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
    return {
        'student_repository': student_repository,
        'learning_result_repository': learning_result_repository,
        'persist_service': persist_service,
        'export_service': export_service,
        'report_template': report_template
    }

def clean_up():
    # Delete temp dir
    shutil.rmtree(Path(TEMP_DIR), ignore_errors=True)
    # pass

def main():
    context = init_context()
    persist_service: PersistService = context.get('persist_service')
    export_service: ExportService = context.get('export_service')
    xlsx_dir = sys.argv[1] if sys.argv and len(sys.argv) > 1 else DEV_NULL_DIR
    target_files = []
    for root, _, files in os.walk(xlsx_dir):
        target_files.extend([os.path.join(root, x) for x in files if x.endswith(XLSX_EXTENSION)])
    for file_path in target_files:
        persist_service.import_workbook(file_path)
    export_service.generate_report()
    clean_up()

if __name__ == '__main__':
    main()
