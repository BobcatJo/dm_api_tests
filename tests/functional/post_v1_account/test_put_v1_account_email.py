
def test_put_v1_account_email(account_helper, mail_api):
    # Изменение email пользователя

    login = 'zx_17_02_2026_11_22_09'
    password = 'alex_1'
    email = f'{login}@ya.ru'

    account_helper.user_login(login=login, password=password)
    account_helper.email_change(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.activation_user(login=login)
    account_helper.user_login(login=login, password=password)


