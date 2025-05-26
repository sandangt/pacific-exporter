import os
from pathlib import Path

XLSX_EXTENSION = '.xlsx'
DEV_NULL_DIR = '/dev/null'
TEMP_DIR = str(Path(os.getcwd(), '.tmp'))
RESULT_DIR = str(Path(os.getcwd(), 'dist'))
RESOURCE_DIR = str(Path(os.getcwd(), 'resources'))
REPORT_TEMPLATE = str(Path(RESOURCE_DIR, 'templates', 'program-report.html'))
DB_FILE_PATH = str(Path(TEMP_DIR, 'data.db'))
TEXT_REPORT_FILE_PATH = str(Path(TEMP_DIR, 'text-report.txt'))
PDF_FILE_PATH = str(Path(RESULT_DIR, 'report.pdf'))
PROGRAM_MANAGER = ['Bad Bunny', 'Chủ Tịch Gà Bông', 'Công Chúa 0 Giờ', 'Hoa Hậu xã', 'Giám Đốc Làng Vũ Đại']
