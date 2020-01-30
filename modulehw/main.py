import datetime
from application import salary, people


if __name__ == '__main__':
    print(datetime.datetime.now())
    salary.calculate_salary()
    print(datetime.datetime.now())
    people.get_employees()
