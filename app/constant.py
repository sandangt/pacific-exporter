import os
import sys
from datetime import date
from enum import Enum
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
FONT_DIR = str(Path(RESOURCE_DIR, 'fonts'))
TEXT_REPORT_FILE_PATH = str(Path(TEMP_DIR, 'text-report.txt'))
FINAL_REPORT_NAME = 'report.pdf'
PROGRAM_MANAGER = ['Bad Bunny', 'Chủ Tịch Gà Bông', 'Công Chúa 0 Giờ', 'Hoa Hậu xã', 'Giám Đốc Làng Vũ Đại']
GIT_KEEP_FILE_NAME = '.gitkeep'
REPORT_TITLE = 'BILINGUAL PROGRAM REPORT'
PROGRAM_MANAGER_TITLE = 'ENGLISH BILINGUAL PROGRAM MANAGER'
TODAY_STR = date.today().strftime("%B %d, %Y")

class CalibriFont(Enum):
    REGULAR = ('Calibri', 'regular', Path(FONT_DIR, 'calibri-regular.ttf'))
    BOLD = ('Calibri-Bold', 'bold', Path(FONT_DIR, 'calibri-bold.ttf'))
    ITALIC = ('Calibri-Italic', 'italic', Path(FONT_DIR, 'calibri-italic.ttf'))
    BOLD_ITALIC = ('Calibri-BoldItalic', 'bold_italic', Path(FONT_DIR, 'calibri-bold-italic.ttf'))

    def __init__(self, font_name: str, style: str, path: Path):
        self.__font_name = font_name
        self.__style = style
        self.__path = path

    @property
    def font_name(self) -> str:
        return self.__font_name

    @property
    def style(self) -> str:
        return self.__style

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def str_path(self) -> str:
        return str(self.__path)

    def path_exists(self) -> bool:
        return self.__path.exists()
