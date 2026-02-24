import allure


@allure.suite('Тесты на проверку метода DELETE v1/login')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка разлогинивания пользователя')

def test_delete_v1_account_auth(auth_account_helper):
        auth_account_helper.logout()