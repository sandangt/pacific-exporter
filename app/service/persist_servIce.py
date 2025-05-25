from typing import List

from openpyxl.utils.cell import column_index_from_string
from openpyxl.worksheet.worksheet import Worksheet

from app.model import LearningResult, Student
from app.repository import StudentRepository, LearningResultRepository
from app.utils import make_student_slug, map_grade


class PersistService:
    def __init__(self, student_repository: StudentRepository, learning_result_repository: LearningResultRepository):
        self._student_repository = student_repository
        self._learning_result_repository = learning_result_repository

    @staticmethod
    def extract_sheet_student(sheet: Worksheet) -> List[Student]:
        class_code = sheet.title
        semester_title = sheet.cell(row=1, column=column_index_from_string('A')).value
        student_list = []
        current = 4
        while no_in_class := sheet.cell(row=current, column=column_index_from_string('A')).value:
            student_name = sheet.cell(current, column=column_index_from_string('B')).value
            student_list.append(Student(
                class_code=class_code,
                semester_title=semester_title,
                slug=make_student_slug(class_code, student_name),
                name=student_name,
                no_in_class=no_in_class,
            ))
            current += 1
        return student_list

    def extract_sheet_learning_result(self, sheet: Worksheet) -> List[LearningResult]:
        teacher_name = sheet.cell(row=2, column=column_index_from_string('D')).value
        class_code = sheet.title
        learning_result_list = []
        current = 4
        while sheet.cell(row=current, column=column_index_from_string('A')).value:
            student_name = sheet.cell(current, column=column_index_from_string('B')).value
            student_slug = make_student_slug(class_code, student_name)
            student_entity = self._student_repository.get_by_slug(student_slug)
            mark = int(sheet.cell(row=current, column=column_index_from_string('D')).value)
            learning_result_list.append(LearningResult(
                mark=mark,
                grade=map_grade(mark),
                teacher_name=teacher_name,
                comment=sheet.cell(row=current, column=column_index_from_string('D')).value,
                student_id=student_entity.id
            ))
            current += 1
        return learning_result_list

    def import_sheet(self, sheet: Worksheet):
        student_list = self.extract_sheet_student(sheet)
        self._student_repository.bulk_upsert(student_list)
        learning_result_list = self.extract_sheet_learning_result(sheet)
        self._learning_result_repository.create_all(learning_result_list)

    def upsert(self, payload: Student):
        pass
