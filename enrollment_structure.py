import datetime

from university_system2 import Student

class EnrollmentRecord:

    key = 'id'

    def __init__(self, student: Student, enroll_date: datetime.date):
        self.student = student
        self.enroll_date = enroll_date

    def __lt__(self, other):
        if EnrollmentRecord.key == 'name':
            return self.student.name < other.student.name
        elif EnrollmentRecord.key == 'date':
            return self.enroll_date < other.enroll_date
        else:
            return self.student.student_id < other.student.student_id
    
    def __gt__(self, other):
        if EnrollmentRecord.key == 'name':
            return self.student.name > other.student.name
        elif EnrollmentRecord.key == 'date':
            return self.student.enroll_date > other.student.enroll_date
        else:
            return self.student.name > other.student.name

    def _repr_(self):
        return f"EnrollmentRecord {self.student.name}, {self.enroll_date}"