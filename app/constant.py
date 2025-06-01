import os
from pathlib import Path

XLSX_EXTENSION = '.xlsx'
TEMP_DIR = str(Path(os.getcwd(), '.tmp'))
DB_FILE_PATH = str(Path(TEMP_DIR, 'data.db'))
RESOURCE_DIR = str(Path(os.getcwd(), 'resources'))
REPORT_TEMPLATE = str(Path(RESOURCE_DIR, 'templates', 'program-report.html'))
TEXT_REPORT_FILE_PATH = str(Path(TEMP_DIR, 'text-report.txt'))
FINAL_REPORT_NAME = 'report.pdf'
PROGRAM_MANAGER = ['Bad Bunny', 'Chủ Tịch Gà Bông', 'Công Chúa 0 Giờ', 'Hoa Hậu xã', 'Giám Đốc Làng Vũ Đại']
