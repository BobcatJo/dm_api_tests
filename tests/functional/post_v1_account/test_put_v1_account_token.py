import datetime
from collections import namedtuple

import pytest

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

@pytest.fixture
def mail_api():
    mail_configuration = MailConfiguration(host='http://185.185.143.231:5025')
    mail_client = Mail_api(configuration=mail_configuration)
    return mail_client

@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051',disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture
def account_helper(account_api, mail_api):
    account_helper = AccountHelper(dm_account_api=account_api, mail=mail_api)
    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'zx_{data}'
    password = 'alex_1'
    email = f'{login}@ya.ru'
    User = namedtuple('User', ["login","password","email"])
    user = User(login=login, password=password, email=email)
    return user

def test_put_v1_account_token(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    # Регистрация пользователя


    account_helper.register_new_user(login=login, password=password, email=email)
