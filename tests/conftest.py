import datetime
import os
import uuid
from collections import namedtuple
import pytest
from vyper import v
from pathlib import Path
from helpers.account_helper import AccountHelper
from packages.notifier.bot import send_file
from packages.restclient.configuration import Configuration as MailConfiguration
from packages.restclient.configuration import Configuration as DmApiConfiguration
from services.api_mail import Mail_api
from services.dm_api_account import DMApiAccount
import structlog
from swagger_coverage_py.reporter import CoverageReporter


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        ),
    ]
)

options = ('service.dm_api_account', 'service.mail', 'user.login' , 'user.password', 'telegram.chat_id', 'telegram.token',)

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://185.185.143.231:5051")
    reporter.setup("/swagger/Account/swagger.json")
    yield
    reporter.generate_report()
    reporter.cleanup_input_files()

@pytest.fixture(scope='function', autouse=True)
def set_config(request):
    config = Path(__file__).joinpath('../../').joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f'{option}', request.config.getoption(f'{option}'))
    os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get("telegram.chat_id")
    os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get("telegram.token")
    request.config.stash['telegram-notifier-addfields']['enviroment'] = config_name
    request.config.stash['telegram-notifier-addfields']['report'] = 'https://bobcatjo.github.io/dm_api_tests/'

def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stg', help='run stg')

    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)

@pytest.fixture(scope='function')
def mail_api():
    mail_configuration = MailConfiguration(host=v.get('service.mail'),disable_log=False)
    mail_client = Mail_api(configuration=mail_configuration)
    return mail_client

@pytest.fixture(scope='function')
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'),disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture(scope='function')
def account_helper(account_api, mail_api):
    account_helper = AccountHelper(dm_account_api=account_api, mail=mail_api)
    return account_helper

@pytest.fixture(scope='function')
def auth_account_helper(mail_api):
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'),disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mail=mail_api)
    account_helper.auth_client(login = v.get('user.login'), password = v.get('user.password'))
    account_helper.default_login = "zx_18_02_2026_13_21_17"
    account_helper.default_password = "alex_1"
    account_helper.default_email = "zx_18_02_2026_13_21_17@ya.ru"
    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.datetime.now()
    data = uuid.uuid4()
    login = f'zx_{data}'
    password = v.get('user.password')
    email = f'{login}@ya.ru'
    User = namedtuple('User', ["login","password","email"])
    user = User(login=login, password=password, email=email)
    return user

