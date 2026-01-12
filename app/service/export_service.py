import random
from pathlib import Path
from typing import List, Dict

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen.canvas import Canvas
from sqlalchemy import UUID
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable, BaseDocTemplate
from reportlab.lib import colors

from app.constant import FINAL_REPORT_NAME, REPORT_TITLE, CalibriFont, PROGRAM_MANAGER_TITLE
from app.dto import PaginationParams, OrderByParams, ReportInfo, ReportComment
from app.exception import ItemNotFoundException
from app.generated_constant import PROGRAM_MANAGER, SIGNING_DATE
from app.repository import StudentRepository, LearningResultRepository


class ExportService:

    __FOOTER_PARAGRAPH_HEIGHT = 15*mm
    __FOOTER_PARAGRAPH_WIDTH = 10*cm

    def __init__(self,
                student_repository: StudentRepository,
                learning_result_repository: LearningResultRepository):
        self.__student_repository = student_repository
        self.__learning_result_repository = learning_result_repository
        self.__styles = self.__create_styles()
        self.__table_styles = self.__create_table_styles()

    def generate_report(self, output_dir: str):
        """Generate PDF report for all students."""
        output_path = Path(output_dir, FINAL_REPORT_NAME)
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=12*mm,
            leftMargin=12*mm,
            topMargin=23*mm,
            bottomMargin=15*mm,
            title=REPORT_TITLE.capitalize()
        )

        elements = []
        order_by = OrderByParams(order='class_code')
        current_page = 0
        while students := self.__student_repository.get_all(PaginationParams(offset=current_page, size=100), order_by):
            for student in students:
                report_info = self.__compile_report_context(student.id)
                elements.extend(self.__build_report_elements(report_info, doc))
            current_page += 1
        doc.build(elements, onFirstPage=self.__build_footer, onLaterPages=self.__build_footer)

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
            comments=comments
        )

    def __build_report_elements(self, report_info: ReportInfo, doc: BaseDocTemplate) -> List[Flowable]:

        title_text = Paragraph(REPORT_TITLE, self.__styles['title'])
        subtitle_text = Paragraph(report_info.semester_title, self.__styles['subtitle'])
        student_info = self.__build_student_info_section(report_info)
        table = self.__build_table_section(report_info, doc)
        comment_section = self.__build_comment_section(report_info)

        return [
            title_text,
            subtitle_text,
            Spacer(1, 10*mm),
            *student_info,
            Spacer(1, 5*mm),
            table,
            Spacer(1, 5*mm),
            *comment_section,
            PageBreak()
        ]

    def __build_student_info_section(self, report_info: ReportInfo) -> List[Flowable]:
        return [
            Paragraph(f'Student\'s name: {report_info.student_name}', self.__styles['student_info']),
            Paragraph(f'Class: {report_info.class_code}', self.__styles['student_info']),
        ]

    def __build_table_section(self, report_info: ReportInfo, doc: BaseDocTemplate) -> Flowable:
        table_data = [
            [Paragraph('SUBJECT', self.__styles['table_column_headers'])] +
            [Paragraph(subject, self.__styles['table_row_subject_name']) for subject in report_info.subjects],

            [Paragraph('TEACHER\'S NAME', self.__styles['table_column_headers'])] +
            [Paragraph(teacher, self.__styles['table_row_teacher_name']) for teacher in report_info.teachers],

            [Paragraph('AVERAGE SCORES', self.__styles['table_column_headers'])] +
            [Paragraph(str(mark), self.__styles['table_row_mark']) for mark in report_info.marks],

            [Paragraph('GRADING', self.__styles['table_column_headers'])] +
            [Paragraph(grade, self.__styles['table_row_mark']) for grade in report_info.grades]
        ]
        num_subjects = len(report_info.subjects)
        available_width = A4[0] - (doc.rightMargin + doc.leftMargin)
        first_col_min_width = 25*mm
        if (available_width / (num_subjects + 1)) > first_col_min_width:
            col_widths = [available_width / (num_subjects + 1)] * (num_subjects + 1)
        else:
            remaining_width = available_width - first_col_min_width
            subject_col_width = max(remaining_width / num_subjects if num_subjects > 0 else 30*mm, 24.5*mm)
            col_widths = [first_col_min_width] + [subject_col_width] * num_subjects
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(self.__table_styles)
        return table

    def __build_comment_section(self, report_info: ReportInfo) -> List[Flowable]:
        comment_section = []
        if report_info.comments:
            for comment in report_info.comments:
                comment_section.extend([
                    Paragraph(
                        f'<b>* {comment.teacher}\'s comments:</b> <i>{comment.text}</i>', self.__styles['comment']
                    ),
                    Spacer(1, 2*mm),
                ])
        return comment_section

    def __build_footer(self, canvas: Canvas, doc: BaseDocTemplate):
        canvas.saveState()
        signature_start_x = doc.width - doc.rightMargin - 8*cm
        p_datetime = Paragraph(f'<i>{SIGNING_DATE}</i>', self.__styles['footer'])
        p_signature_name = Paragraph(f'<b>{PROGRAM_MANAGER.title()}</b>', self.__styles['footer'])
        p_signature_info = Paragraph(f'<b>{PROGRAM_MANAGER_TITLE.upper()}</b>', self.__styles['footer'])

        p_datetime.wrap(self.__FOOTER_PARAGRAPH_WIDTH, self.__FOOTER_PARAGRAPH_HEIGHT)
        p_signature_name.wrap(self.__FOOTER_PARAGRAPH_WIDTH, self.__FOOTER_PARAGRAPH_HEIGHT)
        _, h_signature_info = p_signature_info.wrap(self.__FOOTER_PARAGRAPH_WIDTH, self.__FOOTER_PARAGRAPH_HEIGHT)

        p_datetime.drawOn(canvas, signature_start_x, doc.bottomMargin + 4*cm)
        p_signature_name.drawOn(canvas, signature_start_x, doc.bottomMargin+h_signature_info)
        p_signature_info.drawOn(canvas, signature_start_x, doc.bottomMargin)
        canvas.restoreState()

    @staticmethod
    def __create_styles() -> Dict[str, ParagraphStyle]:
        sample_style = getSampleStyleSheet()
        return {
            'title': ParagraphStyle(
                'Title',
                parent=sample_style['Normal'],
                fontName=CalibriFont.BOLD.font_name,
                fontSize=23,
                spaceAfter=0,
                alignment=TA_CENTER,
                textColor=colors.black,
                leading=28
            ),
            'subtitle': ParagraphStyle(
                'Subtitle',
                parent=sample_style['Normal'],
                fontName=CalibriFont.BOLD.font_name,
                fontSize=15,
                spaceAfter=0,
                alignment=TA_CENTER,
                textColor=colors.black,
                leading=17
            ),
            'student_info': ParagraphStyle(
                'StudentInfo',
                parent=sample_style['Normal'],
                fontName=CalibriFont.BOLD.font_name,
                fontSize=14,
                alignment=TA_LEFT,
                textColor=colors.black,
                leading=17,
            ),
            'table_column_headers': ParagraphStyle(
                'TableColumnHeaders',
                parent=sample_style['Normal'],
                fontName=CalibriFont.BOLD.font_name,
                fontSize=11,
                alignment=TA_CENTER,
                textColor=colors.black,
            ),
            'table_row_subject_name': ParagraphStyle(
                'TableRowSubjectName',
                parent=sample_style['Normal'],
                fontName=CalibriFont.BOLD.font_name,
                fontSize=11,
                alignment=TA_CENTER,
                textColor=colors.black,
            ),
            'table_row_teacher_name': ParagraphStyle(
                'TableRowTeacherName',
                parent=sample_style['Normal'],
                fontName=CalibriFont.REGULAR.font_name,
                fontSize=11,
                alignment=TA_CENTER,
                textColor=colors.black,
            ),
            'table_row_mark': ParagraphStyle(
                'TableRowMark',
                parent=sample_style['Normal'],
                fontName=CalibriFont.BOLD.font_name,
                fontSize=12.5,
                alignment=TA_CENTER,
                textColor=colors.black,
            ),
            'comment': ParagraphStyle(
                'Comment',
                parent=sample_style['Normal'],
                fontName=CalibriFont.REGULAR.font_name,
                fontSize=14,
                alignment=TA_JUSTIFY,
                textColor=colors.black,
                leading=17
            ),
            'footer': ParagraphStyle(
                'Footer',
                parent=sample_style['Normal'],
                fontName=CalibriFont.REGULAR.font_name,
                fontSize=14,
                alignment=TA_CENTER,
                textColor=colors.black,
                leading=17
            ),
        }

    @staticmethod
    def __create_table_styles() -> TableStyle:
        return TableStyle([
            # Base padding for all cells
            ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),

            # Vertical padding - more for rows with larger font sizes
            ('TOPPADDING', (0, 0), (-1, 1), 2*mm),
            ('BOTTOMPADDING', (0, 0), (-1, 1), 2*mm),
            ('TOPPADDING', (0, 2), (-1, -1), 2.5*mm),
            ('BOTTOMPADDING', (0, 2), (-1, -1), 3.5*mm),

            # Alignment
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Borders - solid black grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
