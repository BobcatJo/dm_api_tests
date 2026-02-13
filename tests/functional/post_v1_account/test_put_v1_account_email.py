
def test_put_v1_account_email(account_helper, mail_api):
    # Изменение email пользователя

    login = 'zx_13_02_2026_17_00_40'
    password = 'alex_1'
    email = f'{login}@ya.ru'
    account_helper.user_login(login=login, password=password)
    account_helper.email_change(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    token =  account_helper.get_activation_token_by_login(login=login)
    account_helper.activation_user(token=token)
    account_helper.user_login(login=login, password=password)


