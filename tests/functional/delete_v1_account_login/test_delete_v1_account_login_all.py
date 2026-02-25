import allure


@allure.suite('Тесты на проверку метода DELETE v1/login/all')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка разлогинивания пользователя со всех устройств')

def test_delete_v1_account_all_auth(auth_account_helper):
    auth_account_helper.logout()