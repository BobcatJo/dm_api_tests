from datetime import datetime

from hamcrest import assert_that, \
    has_property, \
    starts_with, \
    all_of, \
    instance_of, \
    has_properties, \
    equal_to

from checkers.http_checkers import check_status_code_http


def test_get_v1_account_auth(auth_account_helper):
    with check_status_code_http():
        response = auth_account_helper.get_account_info()
        assert_that(response,
               has_property("resource",
                            all_of(
                          has_property('login',
                                             starts_with('z')),
                                has_property('registration',
                                             instance_of(datetime)),
                                has_property('rating',
                                             has_properties(
                                                 {
                                                     'enabled': equal_to(True),
                                                     'quality': equal_to(0),
                                                     'quantity': equal_to(0)
                                                 }
                                             )
                                             )
                            )
                            )
               )


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.get_account_info()