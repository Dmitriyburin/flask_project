from requests import get, post, delete, put

# # Получение всех работ
# print(get('http://localhost:5000/api/jobs').json())
#
# # Корректное получение одной работы
# print(get('http://localhost:5000/api/jobs/1').json())
# print(get('http://localhost:5000/api/jobs/2').json())
#
# # Ошибочный запрос на получение одной работы — неверный id
# print(get('http://localhost:5000/api/jobs/1234').json())
#
# # Ошибочный запрос на получение одной работы — строка
# print(get('http://localhost:5000/api/jobs/ghbdtn').json())

# # Корректный POST-запрос
# print(post('http://127.0.0.1:5000/api/jobs',
#            json={'id': 132,
#                  'team_leader': 12,
#                  'job': 'Работа',
#                  'work_size': 100,
#                  'collaborators': '1, 2, 3',
#                  'is_finished': False}).json())
#
# # Некорректные POST-запросы
# # Атрибут json - пуст
# print(post('http://127.0.0.1:5000/api/jobs', json={}).json())
#
# # Отсутствует атрибут json
# print(post('http://127.0.0.1:5000/api/jobs', ).json())
#
# # Переданы не все требуемые поля
# print(post('http://127.0.0.1:5000/api/jobs',
#            json={'id': 132,
#                  'team_leader': 12}).json())
#
# # Получение всех работ
# print(get('http://localhost:5000/api/jobs').json())


# # Тестирование удаления
# # Корректное удаление
# print(delete('http://localhost:5000/api/job/3'))
#
# # Некорректное удаление - неправильный запрос
# print(delete('http://localhost:5000/api/job/'))
#
# # Некорректное удаление - несуществующий ID
# print(delete('http://localhost:5000/api/job/123'))
#
# # Получение всех работ
# print(get('http://localhost:5000/api/jobs').json())


# Тестирование редактирования
# Корректное редактирование
print(put('http://localhost:5000/api/jobs/4',
          json={'team_leader': 12}).json())
# Некорректное редактирование - неправильный запрос
print(put('http://localhost:5000/api/jobs/132'))
# Некорректное редактирование - несуществующий ID
print(put('http://localhost:5000/api/jobs/132',
          json={'team_leader': 12}).json())
