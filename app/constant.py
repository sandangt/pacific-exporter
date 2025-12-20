import os
import sys
from pathlib import Path

def __get_base_path():
    return Path(sys._MEIPASS) if getattr(sys, 'frozen', False) else Path(os.getcwd())

def __get_resource_dir():
    base_path = __get_base_path()
    return str(base_path / 'resources')

def __get_tmp_dir():
    base_path = __get_base_path()
    return str(base_path / 'tmp')

XLSX_EXTENSION = '.xlsx'
RESOURCE_DIR = __get_resource_dir()
TEMP_DIR = __get_tmp_dir()
DB_FILE_PATH = str(Path(TEMP_DIR, 'data.db'))
REPORT_TEMPLATE = str(Path(RESOURCE_DIR, 'templates', 'program-report.html'))
FONT_DIR = str(Path(RESOURCE_DIR, 'fonts'))
TEXT_REPORT_FILE_PATH = str(Path(TEMP_DIR, 'text-report.txt'))
FINAL_REPORT_NAME = 'report.pdf'
PROGRAM_MANAGER = ['Bad Bunny', 'Chủ Tịch Gà Bông', 'Công Chúa 0 Giờ', 'Hoa Hậu xã', 'Giám Đốc Làng Vũ Đại']
GIT_KEEP_FILE_NAME = '.gitkeep'
