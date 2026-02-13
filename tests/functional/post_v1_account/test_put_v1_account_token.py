
def test_put_v1_account_token(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    # Регистрация пользователя


    account_helper.register_new_user(login=login, password=password, email=email)
    token =  account_helper.get_activation_token_by_login(login=login)
    account_helper.activation_user(token=token)
