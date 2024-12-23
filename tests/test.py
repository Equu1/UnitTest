import pytest
import os
from src.student import Student
from src.presence import Attendance

@pytest.fixture
def sample_students():
    Student.list_of_students = []
    Student(0, "Marcin", "Duda")
    Student(1, "Andrzej", "Duda")
    yield
    Student.list_of_students = []

@pytest.fixture
def sample_attendance_file(tmp_path):
    file = tmp_path / "attendance_test.csv"
    with open(file, "w") as f:
        f.write("0,1\n1,0\n")
    return file

@pytest.fixture
def sample_student_file(tmp_path):
    file = tmp_path / "students_test.csv"
    with open(file, "w") as f:
        f.write("0,Marcin,Duda\n1,Andrzej,Duda\n")
    return file

def test_student_save_to_file(tmp_path, sample_students):
    #GIVEN
    file = tmp_path / "students_save_test.csv"
    want = ["0,Marcin,Duda\n", "1,Andrzej,Duda\n"]
    #WHEN
    Student.save_to_file(file)
    with open(file, "r") as f:
        got = f.readlines()
    #THEN
    assert file.exists()
    assert got == want

def test_attendance_save_to_file(tmp_path):
    #GIVEN
    file = tmp_path / "attendance_save_test.csv"
    attendance = Attendance("2024-10-30", [{'id': 0, 'status': True}, {'id': 1, 'status': False}])
    want = ["0,True\n", "1,False\n"]
    #WHEN
    attendance.save_to_file(file)
    with open(file, "r") as f:
        got = f.readlines()
    #THEN
    assert file.exists()
    assert got == want

def test_student_load_from_file(sample_student_file):
    #GIVEN
    Student.list_of_students = []
    #WHEN
    Student.load_from_file(sample_student_file)
    #THEN
    assert len(Student.list_of_students) == 2
    assert Student.list_of_students[0].first_name == "Marcin"
    assert Student.list_of_students[1].surname == "Duda"


def test_attendance_load_from_file(sample_attendance_file):
    #GIVEN
    want = [{'id': 0, 'status': True}, {'id': 1, 'status': False}]
    #WHEN
    attendance = Attendance.load_attendance_from_file(str(sample_attendance_file))
    got = attendance.students_attendance
    #THEN:
    assert attendance is not None
    assert got == want

def test_add_student():
    #GIVEN
    Student.list_of_students = []
    want = {"id": 0, "first_name": "Marcin", "surname": "Duda"}
    #WHEN
    Student.add("Marcin", "Duda")
    got = {"id": Student.list_of_students[0].id,
           "first_name": Student.list_of_students[0].first_name,
           "surname": Student.list_of_students[0].surname}
    #THEN
    assert got == want

def test_get_student():
    #GIVEN
    Student.list_of_students = []
    Student(0, "Marcin", "Duda")
    want = {"id": 0, "first_name": "Marcin", "surname": "Duda"}
    #WHEN:
    got = Student.get(0)
    got = {"id": got.id, "first_name": got.first_name, "surname": got.surname}
    #THEN
    assert got == want

def test_get_id():
    #GIVEN
    Student.list_of_students = []
    Student(0, "Marcin", "Duda")
    want = 1
    #WHEN
    got = Student.get_id()
    #THEN
    assert got == want

def test_update_attendance():
    #GIVEN
    student = Student(0, "Marcin", "Duda")
    student.obecnosci["2024-10-30"] = 1
    want = 0
    #WHEN
    student.obecnosci["2024-10-30"] = 0
    got = student.obecnosci["2024-10-30"]
    #THEN
    assert got == want

def test_check_existing_attendance():
    #GIVEN
    student = Student(0, "Marcin", "Duda")
    student.obecnosci["2024-10-30"] = 1
    want = 1
    #WHEN
    got = student.obecnosci.get("2024-10-30")
    #THEN
    assert got == want