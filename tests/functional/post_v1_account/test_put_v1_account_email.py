from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mail.apis.mail_api import MailApi
from restclient.configuration import Configuration as MailConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        ),
    ]
)

def test_post_v1_account():
    # Регистрация пользователя
    mail_configuration = MailConfiguration(host='http://185.185.143.231:5025')
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mail_api = MailApi(configuration=mail_configuration)

    login = 'q102'
    password = 'alex_1'
    email = f'{login}@ya.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f'Пользователь не создан {response.json()}'

    # Получение письма
    response = mail_api.get_api_v2_messages()
    assert response.status_code == 200, "Письмо не получено"

    # Получение токена
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен не был получен для пользователя {login}"

    # Активация пользователя
    response = account_api.put_v1_account_token(token = token)
    assert response.status_code == 200, f"Пользователь {login},не был активирован"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, "Пользователь {login}, не был авторизован"

    # Изменение email
    json_data = {
        'login': login,
        'password': password,
        'email': f'{login}new@ya.ru',
    }

    response = account_api.put_v1_account_email(json_data)


    # Авторизация после смены email
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(json_data=json_data)


    # Получение письма после смены email
    response = mail_api.get_api_v2_messages()


    # Получение токена после смены email
    token = get_activation_token_by_login(login,response)

    # Активация пользователя после смены email
    response = account_api.put_v1_account_token(token = token)

    # Авторизация после смены email
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(json_data=json_data)


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
