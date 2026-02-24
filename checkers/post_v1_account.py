from datetime import datetime

import allure
from hamcrest import starts_with, \
    assert_that, \
    has_property, \
    all_of, \
    has_properties, \
    equal_to, \
    instance_of

from helpers.account_helper import AccountHelper


class PostV1Account:



    @classmethod
    def check_response_values(cls, response):
        with allure.step('Проверка ответа'):
            today = datetime.now().strftime('%Y-%m-%d')
            assert_that(str(response.resource.registration), starts_with(today))
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
