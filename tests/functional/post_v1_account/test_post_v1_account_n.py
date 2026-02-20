from checkers.http_checkers import check_registration


def test_post_v1_account_check_registration_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = "123455"

    with check_registration(400,'Validation failed'):
        account_helper.register_new_user(login, password, email)


def test_post_v1_account_check_registration_login(account_helper, prepare_user):
    login = 'B'
    password = prepare_user.password
    email = prepare_user.email

    with check_registration(400,'Validation failed'):
        account_helper.register_new_user(login, password, email)


def test_post_v1_account_check_registration(account_helper, prepare_user):
    login = prepare_user.login
    password = 'B'
    email = prepare_user.email

    with check_registration(400,'Validation failed'):
        account_helper.register_new_user(login, password, email)