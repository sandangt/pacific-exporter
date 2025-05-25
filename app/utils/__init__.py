from app.exception.custom_exc import InvalidMarkException


def make_student_slug(class_code: str, name: str):
    return name + '\t' + '|' '\t' + class_code

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
