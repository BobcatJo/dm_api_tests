import allure

@allure.suite('Тесты на проверку метода POST v1/account')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка регистрации нового пользователя без аутенфикации')

def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    # Регистрация пользователя

    account_helper.register_new_user(login=login, password=password, email=email)
