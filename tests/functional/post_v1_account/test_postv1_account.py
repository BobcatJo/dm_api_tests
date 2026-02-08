from json import loads

import requests
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mail.apis.mail_api import MailApi


def test_post_v1_account():
    # Регистрация пользователя
    account_api = AccountApi(
        host='http://185.185.143.231:5051'
    )
    login_api = LoginApi(
        host='http://185.185.143.231:5051'
    )
    mail_api = MailApi(
        host='http://185.185.143.231:5025'
    )
    login = 'wqw_23'
    password = 'alex_1'
    email = f'{login}@ya.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.post_v1_account(
        json_data=json_data
    )
    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 201, f'Пользователь не создан {response.json()}'

    # Получение письма
    response = mail_api.get_api_v2_messages()
    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 200, "Письмо не получено"

    # Получение токена
    token = get_activation_token_by_login(
        login,
        response
    )
    print(
        token
        )
    assert token is not None, f"Токен не был получен для пользователя {login}"

    # Активация пользователя
    response = account_api.put_v1_account_token(
        token = token
    )
    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 200, f"Пользователь {login},не был активирован"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(
        json_data=json_data
    )

    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 200, "Пользователь {login}, не был авторизован"

    # Изменение email
    json_data = {
        'login': login,
        'password': password,
        'email': f'{login}new@ya.ru',
    }

    response = account_api.put_v1_account_email(
        json_data
        )

    print(
        response.status_code
    )
    print(
        response.text
    )
    assert response.status_code == 200, 'Email {email}, не был изменен'

    ...


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(
            item['Content']['Body']
            )
        user_login = user_data['Login']
        if user_login == login:
            print(
                user_login
            )
            token = user_data['ConfirmationLinkUrl'].split(
                '/'
            )[-1]
            print(
                token
            )
    return token
