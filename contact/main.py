class Contact:
    def __init__(self, first_name, last_name, phone, *args, favorites=False, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.favorites = favorites
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        info = f'Имя:{self.first_name}\n' + f'Фамилия: {self.last_name}\n' + f'Телефон: {self.phone}\n'
        if self.favorites is True:
            info += 'В избранных: есть\n'
        else:
            info += 'В избранных: нет\n'
        if self.args or self.kwargs:
            info += 'Дополнительная информация:\n'
            for key, value in self.kwargs.items():
                info += f'\t\t\t{key}: {value}\n'
            if self.args:
                info += '\t\t\t'
                for arg in self.args:
                    info += str(arg) + ', '
                info += '\b\b'
        return info


class PhoneBook:
    def __init__(self, name, contacts=[]):
        self.name = name
        self.contacts = contacts

    def add_contact(self, first_name, last_name, phone, *args, favorites=False, **kwargs):
        self.contacts.append(Contact(first_name, last_name, phone, *args, favorites=favorites, **kwargs))

    def add_contact_interactive(self):
        # для теста использовал ответы Федор Кузьмин +7987654321
        # whatsapp=+7987654321 email=kuzmin@yandex.ru||одногруппник преподаватель
        favor = False
        answer = input('Введите фамилию, имя, номер телефона через пробел:')
        answer = answer.split(' ')
        if len(answer) != 3:
            print('Неверное количество аргументов')
            return False
        if input('Введите Да если хотите ввести дополнительную информацию:').lower() in ['y', 'yes', 'да', 'д', 'хочу',]:
            add_info = input('Сначала введите информацию через = и разделяйте пробелами.\n'
                             'Если надо добавить еще инфорцию без = поставте ||  пишите через пробел.\n'
                             'Пример: telegram=@jhony email=jhony@smith.com||друг одноклассник\n'
                             'или ||друг однокласник')
            add_info = add_info.split('||')
            answer_one = add_info[0].split(' ')
            answer_dict = dict()
            for val in answer_one:
                val_split = val.split('=')
                answer_dict[val_split[0]] = val_split[1]
            if len(add_info) == 2:
                answer_list = add_info[1].split(' ')
            if input('Добавить в избранное?(да/нет)').lower() in ['y', 'yes', 'да', 'д', 'хочу',]:
                favor = True
        return self.add_contact(answer[0], answer[1], answer[2], *answer_list, favorites=favor **answer_dict)

    def delete(self, phone):
        for contact in self.contacts:
            if contact.phone == phone:
                self.contacts.remove(contact)

    def print_book(self):
        for contact in self.contacts:
            print(contact)

    def find_favorites(self):
        result = []
        for contact in self.contacts:
            if contact.favorites is True:
                result.append(contact)
        return result

    def find_by_name(self, first_name, last_name):
        for contact in self.contacts:
            if first_name.lower() == contact.first_name.lower() and last_name.lower() == contact.last_name.lower():
                return contact
        print('Контакт не найден')


def adv_print(*args, **kwargs):
    kwargs = kwargs
    start = '\n'
    result = ''
    sep = ' '
    end = '\n'
    in_file = False
    max_line = 300
    for key in kwargs.keys():
        if key == 'start':
            start = kwargs[key]
        elif key == 'max_line':
            max_line = kwargs[key]+1
        elif key == 'in_file':
            in_file = True
        elif key == 'sep':
            sep = kwargs[key]
        elif key == 'end':
            end = kwargs[key]
    result = sep.join([str(x) for x in args])
    if len(result) > max_line:
        for i in range(0, int(len(result)+int(len(result)/(max_line-1))), max_line):
            result = result[:i] + '\n' + result[i:]
    result = start + result
    if in_file:
        with open('print_out.txt', 'w') as out:
            out.write(result)
    print(result)

def main():
    print('Создаем контакты')
    jhon = Contact('Jhon', 'Smith', '+71234567809',  'aaaa', 111, 'ssss', telegram='@jhony', email='jhony@smith.com')
    ivan = Contact('Ivan', 'Ivanov', '+7123456', favorites=True, email='ivanoviv@google.com')
    print(jhon)
    print('\n\nСоздаем телефонную книгу')
    phonebook = PhoneBook('Phonebook', [jhon, ivan])
    phonebook.add_contact('Petr', 'Petrov', '+792345')
    print('Выводим ее')
    phonebook.print_book()
    phonebook.delete('+792345')
    # phonebook.add_contact_interactive()
    print('\nПоиск\n')
    print(phonebook.find_by_name('Ivan', 'ivanov'))
    phonebook.print_book()
    print(phonebook.find_favorites()[0])
    ar = ['Jhon', 'Smith', '+71234567809',  'aaaa', 111, 'ssss']
    print('\n Проверяем функцию adv_print')
    adv_print(*ar, max_line=20)
    adv_print('1234567890'*3, max_line=6, start='цифры в столбик', in_file=True)

if __name__=='__main__':
    main()