from requests import get, post, delete

# Корректный запрос на вывод всех пользователей
print(get('http://localhost:5000/api/v2/users').json())

# Корректный запрос на вывод одного пользователя
print(get('http://localhost:5000/api/v2/users/1').json())

# Некорректный запрос на вывод одного пользователя - несуществующий ID
# print(get('http://localhost:5000/api/v2/users/123').json())

# Некорректный запрос на вывод одного пользователя - строка
# print(get('http://localhost:5000/api/v2/users/q').json())

# Корректный запрос на добавления пользователя
print(post('http://127.0.0.1:5000/api/v2/users',
           json={
               'name': 'Питонович',
               'school_class': 9,
               'password': 'змеечки',
               'email': 'burindima@123'}).json())

# Некорретный запрос на добавление - неполный атрибут json
# print(post('http://127.0.0.1:5000/api/v2/users',
#            json={
#                  'surname': 'Питон',
#                  'name': 'Питонович',
#                  'age': 100}).json())


# Корректный запрос на удаление
print(delete('http://localhost:5000/api/v2/users/17').json())

# Некорректный запрос на удаление - несуществующий ID
print(delete('http://localhost:5000/api/v2/users/1').json())
