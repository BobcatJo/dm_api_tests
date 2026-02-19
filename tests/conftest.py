import datetime
import uuid
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
@pytest.fixture(scope='function')
def mail_api():
    mail_configuration = MailConfiguration(host='http://185.185.143.231:5025')
    mail_client = Mail_api(configuration=mail_configuration)
    return mail_client

@pytest.fixture(scope='function')
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051',disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture(scope='function')
def account_helper(account_api, mail_api):
    account_helper = AccountHelper(dm_account_api=account_api, mail=mail_api)
    return account_helper

@pytest.fixture(scope='function')
def auth_account_helper(mail_api):
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051',disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mail=mail_api)
    account_helper.auth_client(login = 'zx_18_02_2026_13_21_17', password = 'alex_1')
    account_helper.default_login = "zx_18_02_2026_13_21_17"
    account_helper.default_password = "alex_1"
    account_helper.default_email = "zx_18_02_2026_13_21_17@ya.ru"
    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.datetime.now()
    data = uuid.uuid4()
    login = f'zx_{data}'
    password = 'alex_1'
    email = f'{login}@ya.ru'
    User = namedtuple('User', ["login","password","email"])
    user = User(login=login, password=password, email=email)
    return user

