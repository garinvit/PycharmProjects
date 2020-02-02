from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

pattern_name = re.compile(r'[А-Я][а-я]+')
pattern_org = re.compile(r'[А-Я][А-я]+')
pattern_phone = re.compile(r'(\+7|8)\s?\(?(\d{3})\)?\s?\-?([0-9]{3})\s?\-?([0-9]{2})\s?\-?([0-9]{2})((\s?\(?\(?)?([а-я,\.]{1,})\s?(\d*)\)?)?')
pattern_email = re.compile(r'[a-zA-Z0-9\.]+\@[a-zA-Z0-9]+\.[a-zA-Z]+')
pattern_pos = re.compile(r'([a-zа-яА-Я][а-яА-Я\D\s\–]+[^\+0-9\s]+)+')
contacts = []
for i in contacts_list:
    name = []
    my_string = ' '.join(i) # склеиваем в строку
    fio = re.findall(pattern_name, my_string)[:3]
    if fio:# если не нашли фио или для заголовка
        name.append(fio[0] if fio[0] else '-')
        name.append(fio[1] if fio[1] else '-')
        try:
            name.append(fio[2] if fio[2] else '-')
        except:
            name.append('-')
    else:
        name.append('-')
        name.append('-')
        name.append('-')
    for word in name:
        my_string = re.sub(word, '', my_string, count=0)  # отнимаем фио из строки
    organization = re.search(pattern_org, my_string)
    name.append(organization[0] if organization else '-')
    if organization:
        my_string = re.sub(organization[0], '', my_string, count=0)
    name.append('-')
    subst = "+7(\\2)\\3-\\4-\\5 \\8\\9"
    phone = re.search(pattern_phone, my_string)
    if phone:
        phone = re.sub(r'(\+7|8)\s?\(?(\d{3})\)?\s?\-?([0-9]{3})\s?\-?([0-9]{2})\s?\-?([0-9]{2})((\s?\(?\(?)?([а-я,\.]{1,})\s?(\d*)\)?)?', subst, phone[0], 0, re.MULTILINE)
        my_string = re.sub(r'(\+7|8)\s?\(?(\d{3})\)?\s?\-?([0-9]{3})\s?\-?([0-9]{2})\s?\-?([0-9]{2})((\s?\(?\(?)?([а-я,\.]{1,})\s?(\d*)\)?)?', '', my_string, 0, re.MULTILINE)
    name.append(phone if phone else '-')
    email = re.search(pattern_email, my_string)
    if email:
        my_string = re.sub(pattern_email, '', my_string)
    name.append(email[0] if email else '-')
    position = re.search(pattern_pos, my_string)
    if position:
        name[4] = position[0]
    contacts.append(name)
contacts[0] = contacts_list[0]
for num, name in enumerate(contacts): # поиск, слияние и удаление дубликатов
    for index, name_2 in enumerate(contacts):
        if name[0] == name_2[0] and name[1] == name_2[1] and index != num:
            for i, value in enumerate(name):
                if value == '-':
                    name[i] = name_2[i]
            contacts.pop(index)

for con in contacts:
    print(con)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(contacts)
