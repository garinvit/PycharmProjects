from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Boolean, String, Date, create_engine


# вспомогательныесущности
Base = declarative_base()
engine = create_engine('postgresql://test:test@localhost/vk_db')
Session =sessionmaker(bind=engine)
session =Session()


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

def add_user(**kwargs):

    user = User(**kwargs)
    session.add(user)
    session.commit()

create_all(engine)