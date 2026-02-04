import requests
import pprint
from json import loads


def test_post_v1_account():
    login = 'alex_3'
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
    assert response.status_code == 201, f'Пользователь не создан {response.json}'

    # # Получение письма
    params = {
        'limit': '50',
    }
    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Письмо не получено'

    # Получение токена
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
    assert token is not None, f'Токен не был получен для пользователя {login}'

    # # Активация пользователя
    response = requests.put(f'http://185.185.143.231:5051/v1/account/{token}')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Пользователь {login},не был активирован'

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь {login}, не был авторизован'

    ...
