from vk_api import vk_api
from tables import add_user, session, User
import re
import json


oauth_url = 'https://oauth.vk.com/authorize?client_id=7230720&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,friends&response_type=token&v=5.103'
token =   # в комментариях к работе
vk = vk_api.VkApi(token=token)
api = vk.get_api()
my_id = 68648809


def user_info(id):
    info = api.users.get(user_ids=id, fields='sex, bdate, books, city, education, interests, movies, music, personal')[0]
    # print(info)
    info['return'] = 1
    info = edit_keys(**info)
    print(info)
    info['age_from'], info['age_to'] = map(int, input('Введите диапазон возраста для поиска. Например: 22-27').split('-'))
    if info.get('city'):
        if input('Искать в городе который указан в профиле?Y/n').lower() in ['n', 'no', 'not', 'н', 'нет', 'не', '-']:
            info['city'] = api.database.getCities(country_id=1, q=input('Введите название города?'))['items'][0]['id']
    else:
            info['city'] = api.database.getCities(country_id=1, q=input('Введите название города?'))['items'][0]['id']
    if info['sex'] == 2:
        info['search_sex'] = 1
    elif info['sex'] == 1:
        info['search_sex'] = 2

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


def search(**user_info):
    search = api.users.search(count=1000, city=user_info['city'], age_from=user_info['age_from'], age_to=user_info['age_to'], is_closed=False,\
                    fields='sex, bdate, books, city, education, interests, movies, music, personal', sex=user_info['search_sex'])['items']
    print(len(search))
    for i, inf in enumerate(search):
        # if i < 700: #  для теста
        #     continue
        score = 0
        # print(i)
        inf = edit_keys(**inf)
        # print(i, inf)
        mutual_friend = api.friends.getMutual(source_uid=my_id, target_uid=inf['id'])
        inf['mutual_friend'] = len(mutual_friend)
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
            # if re.match(inf.get('religion'), user_info.get('religion'), re.I):
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
        print(i, score)
        # print(inf)
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


def top_search(number=10):
    users_by_score = session.query(User).order_by(User.score.desc()).all()
    result = []
    for num, user in enumerate(users_by_score):
        if num == number:
            break
        result.append({
            'top': num+1,
            'id': user.id,
            'score': user.score,
            'top_photos': top_photos(user.id)
        })
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump({'result': result}, file)
    return result


def main():
    inf = user_info(68648809)
    search(**inf)
    top_search()


if __name__ == '__main__':
    main()