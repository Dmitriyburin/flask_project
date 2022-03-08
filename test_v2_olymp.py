from requests import get, post, delete, put

# # Корректный запрос на вывод всех пользователей
# print(get('http://localhost:5000/api/v2/olympiads').json())
#
# # Корректный запрос на вывод одного пользователя
# print(get('http://localhost:5000/api/v2/olympiads/3').json())
#
# # Некорректный запрос на вывод одного пользователя - несуществующий ID
# print(get('http://localhost:5000/api/v2/jobs/123').json())
#
# # Некорректный запрос на вывод одного пользователя - строка
# print(get('http://localhost:5000/api/v2/jobs/q').json())
#
# Корректный запрос на добавления пользователя
print(post('http://127.0.0.1:5000/api/v2/olympiads',
           json={'subject_id': 1,
                 'title': 'КРУТОТЕНЬ',
                 'school_class': 9,
                 'description': '1, 2, 3',
                 'duration': 120,
                 'link': 'none'}).json())

# Корректный запрос на изменение пользователя
# print(put('http://127.0.0.1:5000/api/v2/olympiads/1',
#           json={'title': 'Крутая олимпиада 2.0'}).json())

# # Некорретный запрос на добавление - неполный атрибут json
# print(post('http://127.0.0.1:5000/api/v2/users',
#            json={
#                  'team_leader': 12,
#                  'job': 'Работа',
#                  'work_size': 100,}).json())
#
# # Некорретный запрос на добавление - атрибут json отсутствует
# print(post('http://127.0.0.1:5000/api/v2/users').json())
#
# # Корректный запрос на удаление
# print(delete('http://localhost:5000/api/v2/job/1').json())
#
# Некорректный запрос на удаление - несуществующий ID
# print(delete('http://localhost:5000/api/v2/olympiads/3').json())
