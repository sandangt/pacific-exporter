from datetime import datetime
from typing import Any

from app.exception.custom_exc import InvalidMarkException


def make_student_slug(class_code: str, name: str):
    return class_code + '\t' + '|' '\t' + name

def map_grade(mark: float) -> str:
    match mark:
        case val if 9 < val <= 10:
            return 'A'
        case val if 7.5 < val <= 9:
            return 'B'
        case val if 5 < val <= 7.5:
            return 'C'
        case val if 0 <= val <= 5:
            return 'D'
        case _:
            raise InvalidMarkException.default()

def parse_mark(mark: Any) -> float:
    if isinstance(mark, datetime):
        return float(str(mark.day) + '.' + str(mark.month))
    return float(mark)

def parse_subject(cell: str) -> str:
    return cell.split(':')[1].strip()

def parse_teacher(cell: str) -> str:
    return cell.split(':')[1].strip()
