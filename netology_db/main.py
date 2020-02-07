import psycopg2


connect_db = psycopg2.connect("dbname=netology_db user=netology")
cur = connect_db.cursor()

students = [
    {'name': 'Иванов Иван', 'gpa': 4, 'birth': '1998-02-03'},
    {'name': 'Петров Петр', 'gpa': 4.5, 'birth': '1999-03-04'},
    {'name': 'Иванов Петр', 'gpa': 4.2, 'birth': '2000-04-05'},
]

courses = [
    {'name': 'Программирование'},
    {'name': 'Математика'},
    {'name': 'Операционные системы и среды'},
]
student = {'name': 'Другой Студент', 'gpa': 3.9, 'birth': '1999-11-11'}

def create_db(): # создает таблицы
    cur.execute("""
    CREATE TABLE if not exists student (
    id serial PRIMARY KEY not null, 
    name varchar(100) not null, 
    gpa numeric(10, 2), 
    birth timestamp with time zone);
    
    CREATE TABLE if not exists course (
    id serial primary key  not null, 
    name varchar(100) not null);
    
    CREATE TABLE if not exists student_course (
    id serial PRIMARY KEY,
    student_id INTEGER REFERENCES student(id),
    course_id INTEGER REFERENCES  course(id));
    """)
    connect_db.commit()


def get_students(course_id): # возвращает студентов определенного курса
    # cur.execute("select student.name from student_course where student_course.course_id = (%s)", str(course_id))
    cur.execute("""
    select s.id, s.name, c.name 
    from student_course sc
    join student s on s.id = sc.student_id 
    join course c on c.id = sc.course_id
    where c.id = (%s)""", str(course_id))
    course = cur.fetchall()
    print(course)
    return course


def add_courses(courses_id):
    try:
        for course in courses_id:
            cur.execute("insert into course (name) values (%s)", (course['name'], ))

    except Exception as e:
        print(e)
        connect_db.rollback()
    else:
        connect_db.commit()
        print("Курсы добавлены ")


def add_students(course_id, students): # создает студентов и
                                       # записывает их на курс
    try:
        for student in students:
            cur.execute("insert into student (name, gpa, birth) values (%s, %s, %s)", (student['name'], student['gpa'], student['birth']))
            cur.execute("select student.id from student where student.name = (%s)", (student['name'],))
            stud_id = cur.fetchall()[0][0]
            cur.execute("insert into student_course (student_id, course_id ) values (%s, %s)", (stud_id, course_id, ))
    except Exception as e:
        print(e)
        connect_db.rollback()
    else:
        connect_db.commit()
        print("Студенты добавлены")


def add_student(student): # просто создает студента
    cur.execute("insert into student (name, gpa, birth) values (%s, %s, %s)", (student['name'], student['gpa'], student['birth']))
    connect_db.commit()


def get_student(student_id):
    cur.execute("select * from student where student.id = (%s)", str(student_id))
    stud = cur.fetchall()
    print(stud)
    return stud


def main():
    # create_db()
    # add_courses(courses)
    # add_students(1, students)
    # add_student(student)
    # get_student('2')
    get_students(1)

if __name__ == "__main__":
    main()
