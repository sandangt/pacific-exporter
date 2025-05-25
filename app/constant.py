import os
from pathlib import Path

XLSX_EXTENSION = '.xlsx'
DEV_NULL_DIR = '/dev/null'
TEMP_DIR = str(Path(os.getcwd(), '.tmp'))
RESULT_DIR = str(Path(os.getcwd(), 'dist'))
REPORT_TEMPLATE = str(Path(os.getcwd(), 'resources', 'templates', 'program-report.html'))
DB_FILE_PATH = str(Path(TEMP_DIR, 'data.db'))
TEXT_REPORT_FILE_PATH = str(Path(TEMP_DIR, 'text-report.txt'))
PDF_FILE_PATH = str(Path(RESULT_DIR, 'report.pdf'))
