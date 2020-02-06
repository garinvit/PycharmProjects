import csv
import re
import datetime
from pymongo import MongoClient

client = MongoClient()


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        database = client[db]
        artists = database['artists']
        artists.drop()
        for artist in reader:
            for key, value in artist.items():
                if key == "Цена":
                    artist[key] = int(value)
                if key == 'Дата':
                    day_month = list(map(int, value.split('.')))
                    artist[key] = datetime.datetime(2020, day_month[1], day_month[0])
            artists.insert_one(artist)
        return database

def find_cheapest(db):
    """
    Отсортировать билеты из базы по возрастанию цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """
    print('Билеты по возрастанию цены')
    asc_artists_list = list(db.artists.find().sort("Цена", 1))
    for art in asc_artists_list:
        print(art)
    return asc_artists_list


def sort_by_date(db, order=1):
    if order == 1:
        print('Билеты по возрастанию даты мероприятия')
    if order == -1:
        print('Билеты по убыванию даты мероприятия')
    artists_list = list(db.artists.find().sort("Дата", order))
    for art in artists_list:
        print(art)
    return artists_list


def find_by_date_period(period, db):
    print('Билеты за период времени')
    date, date_2 = period.split('-')
    date = list(map(int, date.split('.')))
    date_2 = list(map(int, date_2.split('.')))
    date = datetime.datetime(date[0], date[1], date[2])
    date_2 = datetime.datetime(date_2[0], date_2[1], date_2[2])
    artists_list = list(db.artists.find({"Дата": {"$gte": date, "$lte": date_2}}).sort("Цена"))
    for art in artists_list:
        print(art)
    return artists_list


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """

    regex = re.compile(name)
    find_name = list(db.artists.find({'Исполнитель': regex}).sort("Цена", 1))
    for name in find_name:
        print(name)


if __name__ == '__main__':
    database_artists = read_data('artists.csv', 'netology_db')
    artists = database_artists['artists']
    find_cheapest(database_artists)
    sort_by_date(database_artists, -1)
    find_by_name('[A-Za-z]+', database_artists)
    find_by_date_period('2020.07.1-2020.07.31', database_artists)