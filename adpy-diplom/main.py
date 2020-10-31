from vk_api import vk_api
from tables import add_user, session, User
import re
import json


oauth_url = 'https://oauth.vk.com/authorize?client_id=7230720&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,friends&response_type=token&v=5.103'
token = ''# в комментариях к работе
vk = vk_api.VkApi(token=token)
api = vk.get_api()


def user_info():
    info = api.users.get(fields='sex, bdate, books, city, education, interests, movies, music, personal')[0]
    info['return'] = 1
    info = edit_keys(**info)
    # очистка БД по желанию пользователя
    call_id = api.users.get()[0]['id']
    call_id_list = session.query(User).filter_by(call_id=call_id)
    if call_id_list.all():
        print("Для вашего профиля уже есть данные в БД")
        answer = input('Хотите очистить БД?Y/n').lower()
        if answer in ['y', 'yes', 'д', 'да', '+']:
            call_id_list.delete()
            session.commit()
    else:
        print("Для вашего профиля нет данных в БД")

    info['age_from'], info['age_to'] = map(int, input('Введите диапазон возраста для поиска. Например: 22-27').split('-'))

    if info.get('city'):
        if input('Искать в городе который указан в профиле?Y/n').lower() in ['n', 'no', 'not', 'н', 'нет', 'не', '-']:
            info['city'] = api.database.getCities(country_id=1, q=input('Введите название города?'))['items'][0]['id']
    else:
            info['city'] = api.database.getCities(country_id=1, q=input('Введите название города?'))['items'][0]['id']
    if info.get('sex') == 2:
        info['search_sex'] = 1
    elif info.get('sex') == 1:
        info['search_sex'] = 2
    empty_rec = []
    for rec in ['political', 'religion', 'people_main', 'life_main', 'smoking', 'alcohol']:
        if not info.get(rec):
            empty_rec.append(rec)
    if empty_rec:
        print('У вас пустые следующие поля в профиле:', empty_rec)
        while True:
            answer = input('Хотите их заполнить?Y/n').lower()
            if answer in ['n', 'no', 'not', 'н', 'нет', 'не', '-']:
                for rec in empty_rec:
                    info[rec] = 0
                    if rec == 'religion':
                        info[rec] = 'n/a'
                break
            elif answer in ['y', 'yes', 'д', 'да', '+']:
                for rec in empty_rec:
                    if rec == 'political':
                        print("""
political (integer) — политические предпочтения. Возможные значения:
1 — коммунистические;
2 — социалистические;
3 — умеренные;
4 — либеральные;
5 — консервативные;
6 — монархические;
7 — ультраконсервативные;
8 — индифферентные;
9 — либертарианские.)
""")
                        info[rec] = int(input('Ответ:'))
                    elif rec == 'religion':
                        info[rec] = input('religion (string) — мировоззрение.\nОтвет:')
                    elif rec == 'people_main':
                        info[rec] = int(input("""people_main (integer) — главное в людях. Возможные значения:
1 — ум и креативность;
2 — доброта и честность;
3 — красота и здоровье;
4 — власть и богатство;
5 — смелость и упорство;
6 — юмор и жизнелюбие.
Ответ:"""))
                    elif rec == 'life_main':
                        info[rec] = int(input("""life_main (integer) — главное в жизни. Возможные значения:
1 — семья и дети;
2 — карьера и деньги;
3 — развлечения и отдых;
4 — наука и исследования;
5 — совершенствование мира;
6 — саморазвитие;
7 — красота и искусство;
8 — слава и влияние;
Ответ:"""))
                    elif rec == 'alcohol':
                        info[rec] = int(input("""alcohol (integer) — отношение к  алкоголю. Возможные значения:
1 — резко негативное;
2 — негативное;
3 — компромиссное;
4 — нейтральное;
5 — положительное.
Ответ:"""))
                    elif rec == 'smoking':
                        info[rec] = int(input("""smoking (integer) — отношение к курению. Возможные значения:
1 — резко негативное;
2 — негативное;
3 — компромиссное;
4 — нейтральное;
5 — положительное.
Ответ:"""))
                break
            else:
                print('Не удалось распознать ответ!')
    return info


def edit_keys(**kwargs):
    if kwargs.get('personal'):
        d = kwargs['personal']
        kwargs['political'] = d.get('political')
        kwargs['religion'] = d.get('religion')
        # kwargs['interests'] = d.get('interests')
        kwargs['people_main'] = d.get('people_main')
        kwargs['life_main'] = d.get('life_main')
        kwargs['smoking'] = d.get('smoking')
        kwargs['alcohol'] = d.get('alcohol')
    if kwargs.get('city'):
        kwargs['city'] = kwargs['city']['id']
    del_items = ['is_closed', 'university_name', 'faculty', 'faculty_name', 'graduation', 'education_form',
                 'education_status', 'can_access_closed', 'personal', 'track_code']
    for i in del_items:
        if i in kwargs.keys():
            kwargs.pop(i)
    return kwargs


# def get_user(id):
#     info = api.users.get(user_ids=id, fields='sex, bdate, books, city, education, interests, movies, music, personal')[0]
#     return info

# status = 6  # 1 - не женат/ не замужем; 6 - в активном поиске
# ci = api.database.getCities(country_id=1, need_all=1, count=1000)


def search_exc(**user_info):
    search = api.users.search(count=1000, status=6, city=user_info['city'], age_from=user_info['age_from'], age_to=user_info['age_to'], is_closed=False,\
                    fields='sex, bdate, books, city, education, interests, movies, music, personal', sex=user_info['search_sex'])['items']
    print(len(search))
    for start in range(0,len(search),25):
        end = start + 25
        if end > len(search):
            end = len(search)
        uids = [x['id'] for x in search[start:end]]
        # print(start, end, '\n')
        with open('code.txt') as file:
            code = file.read()
        mutual_friend = api.execute(code=code % (uids, len(uids)))
        # print(mutual_friend)
        for mut_index, index in enumerate(range(start, end)):
            inf = search[index]
            inf = edit_keys(**inf)
            inf['mutual_friend'] = len(mutual_friend[mut_index])
            inf['call_id'] = user_info['id']
            score = 0
            score += inf['mutual_friend']*0.3
            if (inf.get('university') == user_info.get('university')) is True:
                print('univer')
                score += 3
            if inf.get('interests'):
                for band in re.split(r'[;,\s_]+', user_info.get('interests')):
                # for band in user_info.get('interests').split(','):
                    if re.findall(band, f'{inf.get("interests")}', re.I):
                        print('interests')
                        score += 3
                        break
            if inf.get('music'):
                for band in re.split(r'[;,\s_]+',user_info.get('music')):
                    if re.findall(band, inf.get('music'), re.I):
                        print('music')
                        score += 3
                        break
            if inf.get('movies'):
                for band in re.split(r'[;,\s_]+', user_info.get('movies')):
                    if re.findall(band, f'{inf.get("movies")}', re.I):
                        print('movies')
                        score += 2.5
                        break
            if inf.get('books'):
                for band in user_info.get('books').split(','):
                    if re.findall(band, inf.get('books'), re.I):
                        print('books')
                        score += 2.5
                        break
            if inf.get('religion'):
                if inf.get('religion').lower() == user_info.get('religion').lower():
                    score += 1.5
                    print(inf.get('religion'))
                    print(user_info.get('religion'))
            if inf.get('political'):
                if inf.get('political') == user_info.get('political'):
                    print('polit')
                    score += 1.5
            if inf.get('life_main'):
                if inf.get('life_main') == user_info.get('life_main'):
                    print('lm')
                    score += 1.5
            if inf.get('smoking'):
                if inf.get('smoking') == user_info.get('smoking'):
                    print('smoke')
                    score += 1.5
            if inf.get('alcohol'):
                if inf.get('alcohol') == user_info.get('alcohol'):
                    print('alc')
                    score += 1.5
            if inf.get('people_main'):
                if inf.get('people_main') == user_info.get('people_main'):
                    print('pm')
                    score += 1.5
            inf['score'] = score
            print(index, score)
            add_user(**inf)


def top_photos(uid):
    photos = api.photos.get(owner_id=uid, album_id='profile', extended=1)['items']
    photos.sort(key=lambda x: x['likes']['count'])  # сортировка фотографий по лайкам
    top = photos[-3::]
    result = []
    for photo in top:
        for size in photo['sizes']:
            if size['type'] == 'z':
                result.append(size['url'])
    return result


def top_search(number=10, **inf):
    print('Вычисляем результат')
    call_id = api.users.get()[0]['id']
    users_by_score = session.query(User).filter_by(call_id=call_id, city=inf.get("city")).order_by(User.score.desc()).all()
    result = []
    for num, user in enumerate(users_by_score):
        if num == number:
            break
        result.append({
            'top': num+1,
            'id': user.id,
            'link': f'https://vk.com/id{user.id}',
            'score': user.score,
            'top_photos': top_photos(user.id)
        })
    file_name = f'result_{call_id}.json'
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump({'result': result}, file)
        print(f'Результат в файле {file_name}')
    return result


def main():
    inf = user_info()
    search_exc(**inf)
    top_search(**inf)


if __name__ == '__main__':
    main()
