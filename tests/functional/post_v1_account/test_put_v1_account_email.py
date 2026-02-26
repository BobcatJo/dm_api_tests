import allure

@allure.suite('Тесты на проверку метода PUT v1/account/email')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка смены email пользователя')


def test_put_v1_account_email(account_helper, mail_api):
    # Изменение email пользователя

    login = 'zx_344eac14-4488-4ad6-88cc-ee156ef5ef01'
    password = 'alex_1'
    email = f'{login}@ya.ru'

    account_helper.user_login(login=login, password=password)
    account_helper.email_change(login=login, password=password, email=email)
    # account_helper.user_login(login=login, password=password)
    account_helper.activation_user(login=login)
    account_helper.user_login(login=login, password=password)


