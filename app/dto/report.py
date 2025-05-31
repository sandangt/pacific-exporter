from typing import List

from pydantic import BaseModel

class ReportComment(BaseModel):
    teacher: str
    text: str

class ReportInfo(BaseModel):
    semester_title: str
    student_name: str
    class_code: str
    subjects: List[str]
    teachers: List[str]
    marks: List[float]
    grades: List[str]
    comments: List[ReportComment]
    program_manager: str
    today: str
