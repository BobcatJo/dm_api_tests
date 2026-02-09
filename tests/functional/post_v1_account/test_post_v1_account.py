
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
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051',disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mail_api = MailApi(configuration=mail_configuration)

    login = 'cKksq200'
    password = 'alex_1'
    email = f'{login}@ya.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f'Пользователь не создан {response.json()}'