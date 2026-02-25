import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


@allure.suite('Тесты на проверку метода GET v1/account')
@allure.sub_suite('Позитивные тесты')
class TestGetV1Account:
    @allure.title('Проверка получения информации об авторизированном пользователе')

    def test_get_v1_account_auth(self,auth_account_helper):
            response = auth_account_helper.get_account_info()
            GetV1Account.check_response(response)



@allure.suite('Тесты на проверку метода GET v1/account')
@allure.sub_suite('Негативные тесты')
@allure.title('Проверка получения информации об не авторизированном пользователе')


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, 'User must be authenticated'):
         account_helper.get_account_info()