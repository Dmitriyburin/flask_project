from requests import get, post, delete, put

# Получение всех работ
print(get('http://localhost:5000/api/users').json())

# Корректное получение одной работы
print(get('http://localhost:5000/api/users/12').json())


# Корректный POST-запрос
print(post('http://127.0.0.1:5000/api/users',
           json={'id': 1,
                 'surname': 'Питон',
                 'name': 'Питоняха',
                 'age': 100,
                 'position': 'cap',
                 'speciality': 'genius',
                 'address': 'найн',
                 'email': 'питон@python.ru',
                 'password': 'помидары'}).json())


# Корректное удаление
print(delete('http://localhost:5000/api/users/14'))


# Корректное редактирование
print(put('http://localhost:5000/api/users/1',
          json={'age': 15}).json())