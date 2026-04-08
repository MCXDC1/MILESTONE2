import csv
import datetime 
from enrollment_structure import EnrollmentRecord

class Student:
    """Represents an individual student with their courses and attached grades"""

    #Mia
    def __init__(self, student_id: str, name: str):
        """Initializes a student object with an id and the students' name"""
        validate_id = student_id.startswith("STU")

        if validate_id == False:
            raise ValueError(f"{student_id} is not a valid ID! Must start with STU")
        elif len(student_id) != 8:
            raise ValueError(f"{student_id} is not a valid ID! Must be 8 characters long!")
        else:
            self.student_id = student_id

        if not name:
            raise ValueError("You must submit a name!")
        else:
            self.name = name
        self.courses = dict()
        self.grade_points = {
            'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D': 1.0, 'F': 0.0
        }
    
    #Mia
    def __eq__(self, other):
        if isinstance(other, Student):
            return self.student_id == other.student_id
        return False

    #Mia
    def __hash__(self):
        return hash(self.student_id)

    #Mia
    def enroll(self, course, grade: str):
        """Enrolls a student into a course"""
        if grade not in self.grade_points:
            raise ValueError(f"{grade} is not a grade in the system")
        else:
            self.courses[course] = grade
            course.add_student(self)

    #Mia
    def update_grade(self, course, grade: str):
        """Updates a students' grade in a course"""
        if grade not in self.grade_points:
            raise ValueError(f"{grade} is not a grade in the system")
        else:
            self.courses[course] = grade

    #Mia
    def get_courses(self):
        """Returns all courses a student is enrolled in"""
        """Paris"""
        return list(self.courses.keys())

    #Paris
    def calculate_gpa(self):   
        """Calculates a students overall GPA"""

        total_points = 0
        total_credits = 0


        for course, grade in self.courses.items():
            """This loops through all the courses a sudent is enrolled in and multiplys points
            by course credits"""
            total_points += self.grade_points[grade] * course.credits
            total_credits += course.credits 
            """all the credits attempted"""

        if total_credits == 0:
            return 0
        """Gpa"""
        return total_points / total_credits
        

    #Paris
    def get_course_info(self,):
       """Returns a summary of all the courses a student is taking"""
       all_courses = list()
       for course, grade in self.courses.items():
            all_courses.append(f'Course: {course.course_code}, Grade: {grade}, Credits: {course.credits} \n')
            
       return all_courses

from linked import LinkedQueue
from course_algorithms import bubble, insertion

class Course:
    """Represents a single course and the students in it"""
    
    #Mia
    def __init__(self, course_code: str, credits: int, capacity: int):
        """Initializes a Course object with a code, how many credits for the course, and capacity for course"""
        self.course_code = course_code
        self.credits = credits
        self.waitlist = LinkedQueue()
        self.capacity = capacity 
        self.enrolled = list()
        self.enrollment_sorted_by = None

    #Mia
    def add_student(self, student: Student):
        """Adds a students to course roster"""
        if student not in self.students:
            self.enrolled.append(student)
    
    #Mia
    def get_student_count(self):
        """Counts how many students are in a course"""
        return len(self.enrolled)
    
    #Paris
    def request_enroll(self, student, enroll_date):
        for record in self.enrolled:
            if record.student.student_id == student.student_id:
                return  
        if len(self.enrolled) < self.capacity:
            record = EnrollmentRecord(student, enroll_date)
            self.enrolled.append(record)
        else:
            self.waitlist.enqueue(student)

        #ask: If a student is already enrolled, should we ignore the request or raise an exception?

    #Paris
    def drop(self, student_id, enroll_date_for_replacement=None):
        removed = False
        for i, record in enumerate(self.enrolled):
            if record.student.student_id == student_id:
                self.enrolled.pop(i)
                removed = True
                break
        #go through the list, look for this student, if found remove them

        if not removed:
            return
        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()

        
            if enroll_date_for_replacement:
                new_date = enroll_date_for_replacement
            else:
                new_date = datetime.date.today()

            new_record = EnrollmentRecord(next_student, new_date)
            self.enrolled.append(new_record)

        #if someone was removed replace them with the next person in the waitlist
 
    def sort_enrolled(self, by: str, algorithm: str):
        """Sort the enrolled roster by key: name, id or date enrolled \n
        Stores what key the roster is sorted by \n
        Rejects sorting by other methods"""

        by.lower()
        algorithm.lower()

        allowed_methods = ('name', 'id', 'date')

        if by not in allowed_methods:
            raise ValueError("The system can only be sorted by name, id, or date!")

        EnrollmentRecord.key = by

        if algorithm == 'bubble':
            bubble(self.enrolled)
        else:
            insertion(self.enrolled)

        self.enrollment_sorted_by = by

    

class University: 
    """Stores all students and all courses"""

    #Paris
    def __init__ (self):
        """Initializes empty course and student rosters"""
        self.students = {}
        self.courses = {}
    
    
    #Paris
    def load_courses_from_csv(self):
        """Load in course information from csv file"""
        with open('course_catalog.csv', 'r') as f:
            """Opens the csv file and reads the lines as dictionaries"""
            data = csv.DictReader(f)
            for line in data:
                """gets the data from csv and adds the course to university"""
                course_code = line['course_code']
                credits = int(line['credits'])
                self.add_course(course_code, credits)

    
    #Paris
    def load_students_from_csv(self):
        """Load in student information from csv file"""
        with open('university_data.csv', 'r') as f:
            data2 = csv.DictReader(f)
            for line in data2:
                """gets data from csv and creates the student object,
                then splits the list into entrys"""
                student_id =  line['Student ID']
                name = line['Name']
                All_courses = line['Courses']
                student = self.add_student(student_id, name)
                courses = All_courses.split(';')

                for entry in courses:
                    """splits course_code and the grades, grabs the course object, then enrolls the student"""
                    if entry:
                        course_code, grade = entry.split(':')
                        course = self.get_course(course_code)

                        if course:
                            student.enroll(course, grade)


    
    #Paris
    def add_course(self, course_code, credits):
        """Adds a course into course roster"""
        if course_code not in self.courses:
            """adds the course if its not already there. Then stores the course in a dict"""
            course = Course(course_code, credits)
            self.courses[course_code] = course
            return self.courses[course_code]
        else: 
            raise ValueError(f"{course_code} is already in the system!")

    
    #Paris / Mia
    def add_student(self, student_id: str, name: str):
        """Adds a student into student roster"""
        if student_id not in self.students:
            """adds student ID if there isnt one already then stores student using the ID as a key"""
            student = Student(student_id, name)
            self.students[student_id] = student
            return self.students[student_id]
        else:
            raise ValueError(f"{student_id} is already in the system!")
    
    #Paris
    def get_student(self, student_id: str):
        """Returns a student in system"""
        if student_id not in self.students:
            """if a student doesnt exist it returns none else it returns the student object"""
            return None
        return self.students[student_id]
    
    #Paris
    def get_course(self, course_code: str):
        """Returns a course in system"""
        if course_code not in self.courses:
            """if the course doesnt exist it returns none"""
            return None
        return self.courses[course_code]

    
    #Paris 
    def get_course_enrollment(self, course_code: str):
        """Returns the number of students enrolled in a given course"""
        course = self.courses.get(course_code)
        """grabs course object from the dict, then raises an error if 
        the course isnt valid"""
        if course is None:
            raise ValueError(f"{course_code} is not in the system!")
        """counts students"""
        return course.get_student_count()

    #Paris
    def get_students_in_course(self, course_code: str):
        """Returns a list of students enrolled in a given course"""
        course = self.get_course(course_code)
        if course:
            return course.students
        return None

    #Paris
    def get_course_stats(self, course_code: str):
        """Returns mean, median, and mode for a course"""

        course = self.get_course(course_code) 
        """grabs the course object"""
        if course is None or not course.students:
            """if theres no course or students then it returns none"""
            return None

        grade_points = {
            'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D': 1.0, 'F': 0.0
        }
        """just the grades and the goa points"""

        scores = []

        for enrollment in course.students:
            """makes student grades into numeric values for grades"""
            grade = enrollment.student.courses.get(course)
            if grade in grade_points:
                scores.append(grade_points[grade])

        if not scores:
            return None
        
        mean = sum(scores) / len(scores) 
        """mean calculations"""

        scores.sort()
        n = len(scores)
        if n % 2 == 1:
            median = scores[n // 2]
        else:
            median = (scores[n // 2 - 1] + scores[n // 2]) / 2

    
        frequency = {}
        """counts the frequency of scores to find the mode"""
        for score in scores:
            frequency[score] = frequency.get(score, 0) + 1

        mode = max(frequency, key=frequency.get)
        """returns the stats"""
        return {
            "mean": round(mean, 2),
            "median": round(median, 2),
            "mode": mode
        }
    
    #Mia
    def intersect_students(self, course_code1: str, course_code2: str):
        """Print common students in two different courses"""
        course1_students= self.get_students_in_course(course_code1)
        course2_students = self.get_students_in_course(course_code2)
        common_students = set(course1_students) & set(course2_students)
        return list(common_students)

    #Paris
    def get_university_gpa_stats(self):
        """Gets mean and median GPA for all students in a university"""
        students_GPAs = []

        for student in self.students.values():
            """Calcuates the GPA for all every student"""
            students_GPAs.append(student.calculate_gpa())

        if not students_GPAs:
            return None

        mean = sum(students_GPAs) / len(students_GPAs)
        """gets the mean GPA"""

        students_GPAs.sort()
        """Calculates the median GPA"""
        n = len(students_GPAs)

        if n % 2 == 1:
            median = students_GPAs[n // 2]
        else:
            median = (students_GPAs[n // 2 - 1] + students_GPAs[n // 2]) / 2

        return {
            "mean": round(mean, 2),
            "median": round(median, 2)
        
        }
    

    
if __name__ == "__main__":
    """Makes the university object"""
    #Paris
    u = University() 
    """loads CSV file data - course and student data"""
    u.load_courses_from_csv()
    u.load_students_from_csv()


    print("Total students:", len(u.students))
    print("Total courses:", len(u.courses))
    """university info summary"""

    student = u.get_student("STU00001")
    """example student!"""
    print("Student name:", student.name)
    print("GPA:", student.calculate_gpa())
    print("Student courses:", student.get_course_info())

    print("CSE2050 enrollment:", u.get_course_enrollment("CSE2050"))
    """course enrollment"""
    
    stats = u.get_course_stats("CSE2050")
    print("CSE2050 statistics:", stats)
    """shows course stats"""

    gpa_stats = u.get_university_gpa_stats()
    print("University Student GPA statistics:", gpa_stats)
    """shows University GPA stats"""
