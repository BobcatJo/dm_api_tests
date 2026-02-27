import time
from json import loads

import allure

from clients.http.dm_api_account.models.email_change_credentials import EmailChangeCredentials
from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.password_change_post import PasswordChangePost
from clients.http.dm_api_account.models.password_change_put import PasswordChangePut
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from services.dm_api_account import DMApiAccount
from services.api_mail import Mail_api


def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f"Попытка получения токена № {count}")
            token = function(*args,
                             **kwargs)
            count += 1
            if count == 5:
                raise AssertionError('Превышено количество попыток получения токена!')
            if token:
                return token
            time.sleep(1)
    return wrapper


class AccountHelper:

    def __init__(self, dm_account_api: DMApiAccount, mail: Mail_api):
        self.dm_account_api = dm_account_api
        self.mail = mail

    # @allure.step('Авторизация пользователя')
    def auth_client(self, login: str, password: str):
        response = self.user_login(login=login, password=password, validate_response = False)
        token = response.headers.get('x-dm-auth-token')
        self.dm_account_api.account_api.set_headers({'X-Dm-Auth-Token': token})
        self.dm_account_api.login_api.set_headers({'X-Dm-Auth-Token': token})
        return token

    # @allure.step('Регистрация нового пользователя')
    def register_new_user(self, login: str, password: str, email: str):
        registration = Registration(
            login = login,
            email = email,
            password =password
        )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        # assert response.status_code == 201, f'Пользователь не создан {response.json()}'
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time <3,'Время ожидания активации превышено'
        assert token is not None, f"Токен не был получен для пользователя {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    # @allure.step('Получение токена при активации')
    def activation_user(self, login):
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен не был получен для пользователя {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    # @allure.step('Аутентфикация пользователя')
    def user_login(self, login: str, password: str, remember_me: bool=True, validate_response=False,validate_headers=False):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me,
        )
        response= self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials,validate_response=validate_response)
        if validate_headers:
            assert response.headers['x-dm-auth-token'],'Токен для пользователя не получен'
        return response

    # @allure.step('Смена email')
    def email_change(self, login: str, password: str, email: str):
        email_change_credentials = EmailChangeCredentials (
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(email_change_credentials)
        return response

    # @allure.step('Смена пароля')
    def password_change(self, login: str, email: str, password: str, new_password: str):
        password_change_post = PasswordChangePost(
            login=login,
            password=password,
            email=email,
        )
        response = self.dm_account_api.account_api.post_v1_account_password(password_change_post = password_change_post)
        # assert response.status_code == 200, f"Пароль не был сброшен"
        token = self.get_token_by_password_reset(login=login)
        password_change_put = PasswordChangePut(
            login=login,
            token=token,
            oldPassword=password,
            newPassword=new_password,
        )
        response = self.dm_account_api.account_api.put_v1_account_password(password_change_put = password_change_put)
        # assert response.status_code == 200, f"Пароль не был изменен"
        return response

    # @allure.step('Получение токена после сброса пароля ')
    def get_token_by_password_reset(self, login):
        token = None
        response = self.mail.mail_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                link = user_data.get('ConfirmationLinkUri')
                if not link:
                    continue
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
        print(token)
        return token

    # @allure.step('Разлогинивание пользователя')
    def logout(self,**kwargs):
        response = self.dm_account_api.login_api.delete_v1_account_login(**kwargs)
        assert response.status_code == 204, "Не удалось выполнить logout"
        return response

    # @allure.step('Разлогинивание пользователя со всех устройств')
    def logout_all(self, token: str | None, **kwargs):
        headers = kwargs.pop('headers') or {}
        if token:
            headers.update({'X-Dm-Auth-Token': token})
        response = self.dm_account_api.login_api.delete_v1_account_login(headers=headers,**kwargs)
        return response

    # @allure.step('Получение информации о пользователе')
    def get_account_info(self,**kwargs):
        response = self.dm_account_api.account_api.get_v1_account(**kwargs)
        user = UserEnvelope(**response.json())
        return user


    @retrier
    def get_activation_token_by_login(self, login):
        token = None
        response = self.mail.mail_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token