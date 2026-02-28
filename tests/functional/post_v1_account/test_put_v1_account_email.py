import allure

@allure.suite('Тесты на проверку метода PUT v1/account/email')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка смены email пользователя')


def test_put_v1_account_email(account_helper, mail_api):
    # Изменение email пользователя

    login = 'zx_02e5bf8f-d3fd-4039-bd4f-554a6374a3ec'
    password = 'alex_1'
    email = f'{login}@ya.ru'

    account_helper.user_login(login=login, password=password)
    account_helper.email_change(login=login, password=password, email=email)
    # account_helper.user_login(login=login, password=password)
    account_helper.activation_user(login=login)
    account_helper.user_login(login=login, password=password)


