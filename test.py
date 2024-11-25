import pytest
import os
from student import Student
from presence import Attendance

def test_save_to_file():
    # Given
    Student.list_of_students = []
    Student.add("Marcin", "Duda")
    Student.add("Andrzej", "Duda")
    # When
    Student.save_to_file("test_students.csv")
    # Then
    assert os.path.exists("test_students.csv")
    with open("test_students.csv", mode="r") as file:
        content = file.readlines()
        assert content == ["0,Marcin,Duda\n", "1,Andrzej,Duda\n"]

def test_load_from_file():
    # Given
    Student.list_of_students = []
    with open("test_students.csv", mode="w") as file:
        file.write("0,Marcin,Duda\n1,Andrzej,Duda\n")
    # When
    Student.load_from_file("test_students.csv")
    # Then
    assert len(Student.list_of_students) == 2
    assert Student.list_of_students[0].first_name == "Marcin"
    assert Student.list_of_students[0].surname == "Duda"
    assert Student.list_of_students[1].first_name == "Andrzej"
    assert Student.list_of_students[1].surname == "Duda"


def test_add():
    Student.list_of_students = []
    # Given + When
    Student.add("Marcin", "Duda")
    # Then
    student = Student.get(0)
    assert student is not None
    assert student.first_name == "Marcin"
    assert student.surname == "Duda"


def test_load_attendance_from_file():
    # Given
    filename = "30-10-2024.csv"
    with open(filename, mode="w") as file:
        file.write("0,1\n1,1\n2,0\n3,1\n")
    # When
    attendance = Attendance.load_attendance_from_file(filename)
    # Then
    assert attendance is not None
    assert attendance.date == "30-10-2024"
    assert len(attendance.students_attendance) == 4
    assert attendance.students_attendance[0]['id'] == 0
    assert attendance.students_attendance[0]['status'] is True
    assert attendance.students_attendance[1]['id'] == 1
    assert attendance.students_attendance[1]['status'] is True
    assert attendance.students_attendance[2]['id'] == 2
    assert attendance.students_attendance[2]['status'] is False
    assert attendance.students_attendance[3]['id'] == 3
    assert attendance.students_attendance[3]['status'] is True



