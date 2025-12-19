import os
import sys
from pathlib import Path

def get_resource_dir():
    """Get resource directory for both development and PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = Path(sys._MEIPASS)
    else:
        # Running in development
        base_path = Path(os.getcwd())
    return str(base_path / 'resources')


XLSX_EXTENSION = '.xlsx'
TEMP_DIR = str(Path(os.getcwd(), '.tmp'))
DB_FILE_PATH = str(Path(TEMP_DIR, 'data.db'))
RESOURCE_DIR = get_resource_dir()
REPORT_TEMPLATE = str(Path(RESOURCE_DIR, 'templates', 'program-report.html'))
FONT_DIR = str(Path(RESOURCE_DIR, 'fonts'))
TEXT_REPORT_FILE_PATH = str(Path(TEMP_DIR, 'text-report.txt'))
FINAL_REPORT_NAME = 'report.pdf'
PROGRAM_MANAGER = ['Bad Bunny', 'Chủ Tịch Gà Bông', 'Công Chúa 0 Giờ', 'Hoa Hậu xã', 'Giám Đốc Làng Vũ Đại']
