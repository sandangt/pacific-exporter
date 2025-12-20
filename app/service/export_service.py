import random
from datetime import date
from pathlib import Path

from jinja2 import Template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from sqlalchemy import UUID
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

from app.constant import PROGRAM_MANAGER, FINAL_REPORT_NAME, FONT_DIR
from app.dto import PaginationParams, OrderByParams, ReportInfo, ReportComment
from app.exception import ItemNotFoundException
from app.repository import StudentRepository, LearningResultRepository


class ExportService:

    def __init__(self, student_repository: StudentRepository,
                 learning_result_repository: LearningResultRepository, report_template: Template):
        self.__student_repository = student_repository
        self.__learning_result_repository = learning_result_repository
        self.__report_template = report_template
        self.__register_vietnamese_font()

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

    @staticmethod
    def __register_vietnamese_font():
        """Register a font that supports Vietnamese characters."""
        try:
            # Try to use DejaVu Sans (includes Vietnamese)
            # You'll need to include this font file in your project
            font_path = Path(FONT_DIR, "DejaVuSans.ttf")
            font_bold_path = Path(FONT_DIR, "DejaVuSans-bold.ttf")

            if font_path.exists():
                pdfmetrics.registerFont(TTFont('DejaVu', str(font_path)))
            if font_bold_path.exists():
                pdfmetrics.registerFont(TTFont('DejaVu-Bold', str(font_bold_path)))

        except Exception as e:
            print(f"Warning: Could not load custom font: {e}")
            print("Falling back to default fonts (Vietnamese may not display correctly)")

    @staticmethod
    def __build_report_elements(report_info: ReportInfo):
        """Build reportlab elements for a single student report."""
        styles = getSampleStyleSheet()

        # Create custom styles with Vietnamese font support
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=1,  # Center alignment
            fontName='DejaVu-Bold',
            spaceAfter=12
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontName='DejaVu-Bold',
            fontSize=14
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName='DejaVu',
            fontSize=11
        )

        bold_normal_style = ParagraphStyle(
            'BoldNormal',
            parent=normal_style,
            fontName='DejaVu-Bold'
        )

        elements = []

        # Title
        elements.append(Paragraph(f"{report_info.semester_title} - Academic Report", title_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Student Info
        elements.append(Paragraph(f"<b>Student:</b> {report_info.student_name}", normal_style))
        elements.append(Paragraph(f"<b>Class:</b> {report_info.class_code}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Results Table
        elements.append(Paragraph("Learning Results", heading_style))
        elements.append(Spacer(1, 0.1 * inch))

        table_data = [['Subject', 'Teacher', 'Mark', 'Grade']]
        for i in range(len(report_info.subjects)):
            table_data.append([
                report_info.subjects[i],
                report_info.teachers[i],
                str(report_info.marks[i]),
                report_info.grades[i]
            ])

        table = Table(table_data, colWidths=[2.5 * inch, 2 * inch, 1 * inch, 1 * inch])
        table.setStyle(TableStyle([
            # Header row styling
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVu-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),

            # Data rows styling
            ('FONTNAME', (0, 1), (-1, -1), 'DejaVu'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

            # Alignment
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Borders - simple black grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3 * inch))

        # Comments section
        if report_info.comments:
            elements.append(Paragraph("Teacher Comments", heading_style))
            elements.append(Spacer(1, 0.1 * inch))
            for comment in report_info.comments:
                elements.append(Paragraph(f"<b>{comment.teacher}:</b> {comment.text}", normal_style))
                elements.append(Spacer(1, 0.1 * inch))

        # Footer
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph(f"<i>Generated on {report_info.today}</i>", normal_style))
        elements.append(Paragraph(f"<i>Program Manager: {report_info.program_manager}</i>", normal_style))
        elements.append(PageBreak())
        return elements

    def generate_report(self, output_dir: str):
        output_path = Path(output_dir, FINAL_REPORT_NAME)
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        elements = []

        order_by = OrderByParams(order='class_code')
        current_offset = 0

        while students := self.__student_repository.get_all(
            PaginationParams(offset=current_offset, size=100), order_by):
            for student in students:
                report_info = self.__compile_report_context(student.id)
                elements.extend(self.__build_report_elements(report_info))
            current_offset += 1

        doc.build(elements)
