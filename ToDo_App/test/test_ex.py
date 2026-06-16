import pytest


# When working with pytest we need to let the parser knows that this is a test function.
def test_equal_or_not_equal():
    assert 10 == 10


def test_instance():
    assert isinstance("Hello how are you", str)
    assert isinstance(2, int)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


# We can only use fixture if we import pytest
@pytest.fixture()
def default_employee():
    return Student("John", "Doe", "Computer Science", 4)


# Here I am using pytest fixture
def test_person_initialization(default_employee):
    assert default_employee.first_name == "John"
    assert default_employee.last_name == "Doe"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 4


"""
    This is what it looks like without the pytest fixture

def test_person_initialization():
    p = Student("John", "Doe", "Computer Science", 4)
    assert p.first_name == "John"
    assert p.last_name == "Doe"
    assert p.major == "Computer Science"
    assert p.years == 4
"""
