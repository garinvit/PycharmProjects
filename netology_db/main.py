import psycopg2


connect_db = psycopg2.connect("dbname=netology_db user=netology")
cur = connect_db.cursor()

students = [
    {'id': 1, 'name': 'Иванов Иван', 'gpa': 4, 'birth': '1998-02-03'},
    {'id': 2, 'name': 'Петров Петр', 'gpa': 4.5, 'birth': '1999-03-04'},
    {'id': 3, 'name': 'Иванов Петр', 'gpa': 4.2, 'birth': '2000-04-05'},
]
student =  {'id': 4, 'name': 'Другой Студент', 'gpa': 3.9, 'birth': '1999-11-11'}

def create_db(): # создает таблицы
    cur.execute("""
    CREATE TABLE student (
    id serial PRIMARY KEY not null, 
    name varchar(100) not null, 
    gpa numeric(10, 2), 
    birth timestamp with time zone);
    
    CREATE TABLE course (
    id serial primary key  not null, 
    name varchar(100) not null,
    primary key (id, name));
    
    CREATE TABLE student_course (
    id serial primary key  not null, 
    name varchar(100) not null,
    primary key (id, name))
    birth timestamp;
    
     
    """)
    connect_db.commit()


def get_students(course_id): # возвращает студентов определенного курса
    cur.execute("select name from course where course.id = (%s)", str(course_id))
    course = cur.fetchall()
    print(course)
    return course


def get_students_add_birth(course_id):
    cur.execute("""
    select student.id, student.name, student.birth, course.id
    from course
    inner join student on course.name = student.name
    where course.id = (%s)""", str(course_id))
    course = cur.fetchall()
    print(course)
    return course


def add_students(course_id, students): # создает студентов и
                                       # записывает их на курс
    try:
        for student in students:
            cur.execute("insert into student (id, name, gpa, birth) values (%s, %s, %s, %s)", (student['id'], student['name'], student['gpa'], student['birth']))
            cur.execute("insert into course (id, name) values (%s, %s)", (course_id, student['name']))
    except Exception as e:
        print(e)
        connect_db.rollback()
    else:
        connect_db.commit()
        print("Студенты добавлены")


def add_student(student): # просто создает студента
    cur.execute("insert into student (id, name, gpa, birth) values (%s, %s, %s, %s)", (student['id'], student['name'], student['gpa'], student['birth']))
    connect_db.commit()


def get_student(student_id):
    cur.execute("select * from student where student.id = (%s)", str(student_id))
    stud = cur.fetchall()
    print(stud)
    return stud


def main():
    create_db()
    add_students(1, students)
    add_student(student)
    get_student('2')
    get_students(1)
    get_students_add_birth(1)


if __name__ == "__main__":
    main()
