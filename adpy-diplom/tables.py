from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine


# вспомогательныесущности
Base = declarative_base()
engine = create_engine('postgresql://sgenby:rjywtynhfnjh@localhost/vk_db')
Session =sessionmaker(bind=engine)
session =Session()


def create_all(engine):
    '''СоздатьвсетаблицывБД'''
    Base.metadata.create_all(engine)

"""
[{'id': 68648809, 'first_name': 'Виталий', 'last_name': 'Гарин', 'is_closed': True, 'can_access_closed': True, 'sex': 2,
 'bdate': '11.5.1993', 'city': {'id': 126, 'title': 'Северск'}, 'university': 852, 'university_name': 'ТУСУР (бывш. ТАСУР, ТИАСУР)', 
 'faculty': 118835, 'faculty_name': 'Факультет систем управления', 'graduation': 2017, 'education_form': 'Заочное отделение', 'education_status': 'Студент (бакалавр)', 
 'personal': {'political': 4, 'langs': ['Русский'], 'religion': 'Атеист', 
 'inspired_by': 'Музыка', 'people_main': 0, 'life_main': 5, 'smoking': 2, 'alcohol': 2}, 
 'interests': 'Музыка', 'music': 'Metallica, Slayer, Megadeath, Rage, Judas Priest  AC/DC, Cavalera Conspiracy, Darkane, Dethklok, Disturbed, Pantera',
'movies': 'Пролетая над гнездом кукушки', 
  'books': 'Лафкрафт "Зов Ктулху", Войнович "Жизнь и необычные приключения солдата Ивана Чонкина", Ричард Докинз "Бог как иллюзия"'}]
"""
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    sex = Column(Integer)
    bdate = Column(Date)
    city = Column(Integer)
    university = Column(Integer)
    political = Column(Integer)
    religion = Column(String(100))
    interests = Column(String(300))
    people_main = Column(Integer)
    life_main = Column(Integer)
    smoking = Column(Integer)
    alcohol = Column(Integer)
    music = Column(String(300))
    movies = Column(String(300))
    books = Column(String(300))
    score = Column(Integer)

    def __init__(self, id, first_name, last_name, sex, bdate, city, university, political, religion, interests, people_main, life_main, smoking, alcohol, music, movies, books, score):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.bdate = bdate
        self.city = city
        self.university = university
        self.political = political
        self.religion = religion
        self.interests = interests
        self.people_main = people_main
        self.life_main = life_main
        self.smoking = smoking
        self.alcohol = alcohol
        self.music = music
        self.movies = movies
        self.books = books
        self.score = score

def add_user(id, first_name, last_name, sex, bdate, city, university, political, religion, interests, people_main, life_main, smoking, alcohol, music, movies, books, score):
    user = User(id, first_name, last_name, sex, bdate, city, university, political, religion, interests, people_main, life_main, smoking, alcohol, music, movies, books, score)
    session.add(user)
    session.commit()

create_all(engine)