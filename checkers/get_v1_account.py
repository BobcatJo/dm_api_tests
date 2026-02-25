from datetime import datetime

import allure
from hamcrest import assert_that, \
    has_property, \
    all_of, \
    starts_with, \
    has_properties, \
    equal_to, \
    instance_of

from dm_api_account.models.user_envelope import UserEnvelope


class GetV1Account:

    @classmethod
    def check_response(cls, response):
        with allure.step('Проверка ответа'):
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