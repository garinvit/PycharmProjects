from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Boolean, String, Date, create_engine


Base = declarative_base()
engine = create_engine('postgresql://test:test@localhost/vk_db')
if not database_exists(engine.url):
    create_database(engine.url)
Session = sessionmaker(bind=engine)
session = Session()


def create_all(engine):
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    sex = Column(Integer)
    bdate = Column(String(50))
    city = Column(Integer)
    university = Column(Integer)
    political = Column(Integer)
    religion = Column(String())
    interests = Column(String())
    people_main = Column(Integer)
    life_main = Column(Integer)
    smoking = Column(Integer)
    alcohol = Column(Integer)
    music = Column(String())
    movies = Column(String())
    books = Column(String())
    mutual_friend = Column(Integer())
    score = Column(Float)
    call_id = Column(Integer())


def add_user(**kwargs):
    user = User(**kwargs)
    try:
        session.add(user)
        session.commit()
    except:
        session.rollback()
        print("Такой человек уже есть в базе данных")


create_all(engine)