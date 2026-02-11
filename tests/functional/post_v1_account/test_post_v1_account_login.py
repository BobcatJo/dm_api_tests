

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mail import Mail_api
from services.dm_api_account import DMApiAccount
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

def test_post_v1_account_login():
    # Регистрация пользователя
    mail_configuration = MailConfiguration(host='http://185.185.143.231:5025')
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051',disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    mail = Mail_api(configuration=mail_configuration)
    account_helper = AccountHelper(dm_account_api=account, mail=mail)
    login = 'zx10228'
    password = 'alex_1'
    email = f'{login}@ya.ru'
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)