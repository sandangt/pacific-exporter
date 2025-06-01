import random
from datetime import date
from pathlib import Path

from jinja2 import Template
from sqlalchemy import UUID
from weasyprint import HTML

from app.constant import TEXT_REPORT_FILE_PATH, PROGRAM_MANAGER, FINAL_REPORT_NAME
from app.dto import PaginationParams, OrderByParams, ReportInfo, ReportComment
from app.exception import ItemNotFoundException
from app.repository import StudentRepository, LearningResultRepository


class ExportService:

    __HTML_PAGE_BREAKER = '<div class="page-break"></div>'

    def __init__(self, student_repository: StudentRepository,
                 learning_result_repository: LearningResultRepository, report_template: Template):
        self.__student_repository = student_repository
        self.__learning_result_repository = learning_result_repository
        self.__report_template = report_template

    def __compile_report_context(self, student_id: UUID) -> ReportInfo:
        student = self.__student_repository.get_one_by_id(student_id)
        if not student:
            raise ItemNotFoundException.student()
        subjects, teachers, marks, grades, comments = [], [], [], [], []
        for i in student.learning_results:
            subjects.append(i.subject)
            teachers.append(i.teacher_name)
            marks.append(i.mark)
            grades.append(i.grade)
            if i.comment:
                comments.append(ReportComment(teacher=i.teacher_name, text=i.comment))
        return ReportInfo(
            semester_title=student.semester_title,
            student_name=student.name,
            class_code=student.class_code,
            subjects=subjects,
            teachers=teachers,
            marks=marks,
            grades=grades,
            comments=comments,
            today=date.today().strftime("%B %d, %Y"),
            program_manager=random.choice(PROGRAM_MANAGER)
        )

    def generate_report(self, output_dir: str):
        order_by = OrderByParams(order='class_code')
        current_offset = 0
        while students := self.__student_repository.get_all(PaginationParams(offset=current_offset, size=100), order_by):
            for student in students:
                html_content = self.__report_template.render(**self.__compile_report_context(student.id).model_dump()) \
                               + self.__HTML_PAGE_BREAKER
                with open(TEXT_REPORT_FILE_PATH, 'a', encoding='utf-8') as f:
                    f.write(html_content)
            current_offset += 1
        HTML(TEXT_REPORT_FILE_PATH).write_pdf(Path(output_dir, FINAL_REPORT_NAME))
