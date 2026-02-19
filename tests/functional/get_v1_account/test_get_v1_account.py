from datetime import datetime
from assertpy import assert_that, soft_assertions

# from hamcrest import assert_that, \
#     equal_to, \
#     starts_with, \
#     all_of, \
#     instance_of, \
#     has_properties, \
#     has_property

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_envelope import UserRole


def test_get_v1_account_auth(auth_account_helper):
    # with check_status_code_http():
        response = auth_account_helper.get_account_info()
        with soft_assertions():
            assert_that(response.resource.login).is_equal_to('zx_18_02_2026_13_21_17')
            print('Прошла проверка логина')
            assert_that(response.resource.online).is_instance_of(datetime)
            print('Прошла проверка даты')
            assert_that(response.resource.roles).contains(UserRole.GUEST,UserRole.PLAYER )
            print('Прошла проверка ролей')
        # assert_that(response,
        #        has_property("resource",
        #                     all_of(
        #                   has_property('login',
        #                                      starts_with('z')),
        #                         has_property('registration',
        #                                      instance_of(datetime)),
        #                         has_property('rating',
        #                                      has_properties(
        #                                          {
        #                                              'enabled': equal_to(True),
        #                                              'quality': equal_to(0),
        #                                              'quantity': equal_to(0)
        #                                          }
        #                                      )
        #                                      )
        #                     )
        #                     )
        #        )


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.get_account_info()