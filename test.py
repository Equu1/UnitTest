import pytest
from unittest.mock import mock_open, patch
from student import Student
from presence import Attendance


class TestStudent:
    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_file(self, mock_file):
        # Given
        Student.list_of_students = []
        Student.add("Marcin", "Duda")
        Student.add("Andrzej", "Duda")

        # When
        Student.save_to_file("test_students.csv")

        # Then
        mock_file.assert_called_once_with("test_students.csv", mode="w", newline="")
        handle = mock_file()

        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        expected_data = "0,Marcin,Duda\r\n1,Andrzej,Duda\r\n"
        assert written_data == expected_data

    @patch("builtins.open", new_callable=mock_open, read_data="0,Marcin,Duda\n1,Andrzej,Duda\n")
    def test_load_from_file(self, mock_file):
        # Given
        Student.list_of_students = []

        # When
        Student.load_from_file("test_students.csv")

        # Then
        assert len(Student.list_of_students) == 2
        assert Student.list_of_students[0].first_name == "Marcin"
        assert Student.list_of_students[0].surname == "Duda"
        assert Student.list_of_students[1].first_name == "Andrzej"
        assert Student.list_of_students[1].surname == "Duda"

    def test_add_student(self):
        # Given
        Student.list_of_students = []

        # When
        Student.add("Marcin", "Duda")

        # Then
        student = Student.get(0)
        assert student is not None
        assert student.first_name == "Marcin"
        assert student.surname == "Duda"


class TestAttendance:
    @patch("builtins.open", new_callable=mock_open, read_data="0,1\n1,1\n2,0\n3,1\n")
    def test_load_attendance_from_file(self, mock_file):
        # Given
        filename = "30-10-2024.csv"

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
