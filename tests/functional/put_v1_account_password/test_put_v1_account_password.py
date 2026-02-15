

def test_put_v1_account_password(auth_account_helper, account_helper):
    login = auth_account_helper.default_login
    password = auth_account_helper.default_password
    email = auth_account_helper.default_email



    auth_account_helper.password_reset(login=login,email=email)
    token = account_helper.get_token_by_password_reset(login=login)
    auth_account_helper.password_change(login=login,token=token,password=password,new_password=f"{password}_new")
    new_password = f"{password}_new"
    auth_account_helper.user_login(login=login,password=new_password)

