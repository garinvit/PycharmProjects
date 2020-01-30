import datetime
from application.people import *
from application.salary import *


if __name__ == '__main__':
    print(datetime.datetime.now())
    calculate_salary()
    print(datetime.datetime.now())
    get_employees()
