from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from app.constant import CalibriFont


def init_font_config():
    __register_calibri_font()

def __register_calibri_font():
    for item in CalibriFont:
        if item.path_exists():
            pdfmetrics.registerFont(TTFont(item.font_name, item.str_path))
    pdfmetrics.registerFontFamily(
        CalibriFont.REGULAR.font_name,
        normal=CalibriFont.REGULAR.font_name,
        bold=CalibriFont.BOLD.font_name,
        italic=CalibriFont.ITALIC.font_name,
        boldItalic=CalibriFont.BOLD_ITALIC.font_name,
    )
