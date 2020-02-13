from vk_api import vk_api
from tables import add_user


oauth_url = 'https://oauth.vk.com/authorize?client_id=7230720&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.103'
token = '270270809f822883858a552baf2f5308fac993f495a756526df5436342048081c15d26499ffe252f31faf'
vk = vk_api.VkApi(token=token)
api = vk.get_api()

def user_info(id):
    info = api.users.get(user_ids=id, fields='sex, bdate, books, city, education, interests, movies, music, personal')
    return info[0]

# search = api.users.search(count=1000, is_closed=False)['items']


status = 6  # 1 - не женат/ не замужем; 6 - в активном поиске
# print(api.database.getCities(country_id=1, q='Омск')['items'][0]['id'])
# ci = api.database.getCities(country_id=1, need_all=1, count=1000)

def search_111():
    pass

inf = user_info(68648809)
a = user_info(60029197)
b = user_info(33457051)
add_user(id=inf.get('id'), first_name=inf.get('first_name'), last_name=inf.get('last_name'), sex=inf.get('sex'), bdate=inf.get('bdate'), city=inf.get('city').get('id'), university=inf.get('university'), \
         political=inf.get('personal').get('political'), religion=inf.get('personal').get('religion'), interests=inf.get('interests'), people_main=inf.get('personal').get('people_main'),\
         life_main=inf.get('personal').get('life_main'), smoking=inf.get('personal').get('smoking'), alcohol=inf.get('personal').get('alcohol'), music=inf.get('music'), movies=inf.get('movies'), books=inf.get('books'), score=0)

