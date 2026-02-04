import requests


def test_post_v1_account():
    login = 'alex_1'
    password = 'alex_1'
    email = f'{login}@ya.ru'
    # Регистрация пользователя
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # Получение письма
    params = {
        'limit': '50',
    }
    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    # Получение токена

    # Активация пользователя
    response = requests.put('http://185.185.143.231:5051/v1/account/1e7d94ce-7fc9-49ad-b64d-bac1eac0be82')
    print(response.status_code)
    print(response.text)

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    ...
