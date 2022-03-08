from requests import get, post, delete

# Корректный запрос на вывод всех пользователей
print(get('http://localhost:5000/api/v2/jobs').json())

# Корректный запрос на вывод одного пользователя
print(get('http://localhost:5000/api/v2/jobs/1').json())

# Некорректный запрос на вывод одного пользователя - несуществующий ID
print(get('http://localhost:5000/api/v2/jobs/123').json())

# Некорректный запрос на вывод одного пользователя - строка
print(get('http://localhost:5000/api/v2/jobs/q').json())

# Корректный запрос на добавления пользователя
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={'team_leader': 1,
                 'job': 'Работа',
                 'work_size': 100,
                 'collaborators': '1, 2, 3',
                 'is_finished': False}).json())

# Некорретный запрос на добавление - неполный атрибут json
print(post('http://127.0.0.1:5000/api/v2/users',
           json={
                 'team_leader': 12,
                 'job': 'Работа',
                 'work_size': 100,}).json())

# Некорретный запрос на добавление - атрибут json отсутствует
print(post('http://127.0.0.1:5000/api/v2/users').json())

# Корректный запрос на удаление
print(delete('http://localhost:5000/api/v2/job/1').json())

# Некорректный запрос на удаление - несуществующий ID
print(delete('http://localhost:5000/api/v2/jobs/123').json())
