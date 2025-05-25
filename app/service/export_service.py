from datetime import date
from pathlib import Path

from jinja2 import Template
from sqlalchemy import UUID
from weasyprint import HTML

from app.constant import PDF_FILE_PATH, TEXT_REPORT_FILE_PATH
from app.dto.list_query import PaginationParams, OrderByParams
from app.dto.report import ReportContext, ReportComment
from app.exception.custom_exc import ItemNotFoundException
from app.repository import StudentRepository, LearningResultRepository


class ExportService:

    __HTML_PAGE_BREAKER = '<div class="page-break"></div>'

    def __init__(self, student_repository: StudentRepository,
                 learning_result_repository: LearningResultRepository, report_template: Template):
        self._student_repository = student_repository
        self._learning_result_repository = learning_result_repository
        self._report_template = report_template

    def compile_report_context(self, student_id: UUID) -> ReportContext:
        student = self._student_repository.get_one_by_id(student_id)
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
        return ReportContext(
            semester_title=student.semester_title,
            student_name=student.name,
            class_code=student.class_code,
            subjects=subjects,
            teachers=teachers,
            marks=marks,
            grades=grades,
            comments=comments,
            today=date.today().strftime("%B %d, %Y"),
            program_manager='Bad Bunny'
        )

    def print_report(self):
        pagination, order_by = PaginationParams(offset=0, size=100), OrderByParams(order='name')
        students = self._student_repository.get_all(pagination, order_by)
        for student in students:
            html_content = self._report_template.render(**self.compile_report_context(student.id).model_dump()) \
                           + self.__HTML_PAGE_BREAKER
            with open(TEXT_REPORT_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(html_content)
        HTML(TEXT_REPORT_FILE_PATH).write_pdf(PDF_FILE_PATH)
