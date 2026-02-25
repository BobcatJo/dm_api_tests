import allure

@allure.suite('Тесты на проверку метода PUT v1/account/email')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка смены email пользователя')


def test_put_v1_account_email(account_helper, mail_api):
    # Изменение email пользователя

    login = 'zx_c3c38cd6-ae0d-4d9e-8d93-2df017da0c76'
    password = 'alex_1'
    email = f'{login}@ya.ru'

    account_helper.user_login(login=login, password=password)
    account_helper.email_change(login=login, password=password, email=email)
    # account_helper.user_login(login=login, password=password)
    account_helper.activation_user(login=login)
    account_helper.user_login(login=login, password=password)


