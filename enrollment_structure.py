import datetime

from university_system2 import Student

class EnrollmentRecord:

    def __init__(self, student: Student, enroll_date: datetime.date):
        self.student = student
        self.enroll_date = enroll_date

    def __lt__(self, other):
        return self.student.student_id < other.student.student_id
    
    def __gt__(self, other):
        return self.student.student_id > other.student.student_id

    def _repr_(self):
        return f"EnrollmentRecord {self.student.name}, {self.enroll_date}"