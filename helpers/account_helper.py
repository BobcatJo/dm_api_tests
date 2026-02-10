from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mail import  Mail_api


class AccountHelper:

    def __init__(self, dm_account_api: DMApiAccount, mail: Mail_api):
        self.dm_account_api = dm_account_api
        self.mail = mail

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не создан {response.json()}'
        response = self.mail.mail_api.get_api_v2_messages()
        assert response.status_code == 200, "Письмо не получено"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Токен не был получен для пользователя {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Пользователь {login},не был активирован"
        return response

    def user_login(self, login: str, password: str, remember_me: bool=True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe':remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь {login}, не был авторизован"
        return response

    def email_change(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не создан {response.json()}'
        response = self.mail.mail_api.get_api_v2_messages()
        assert response.status_code == 200, "Письмо не получено"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Токен не был получен для пользователя {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Пользователь {login},не был активирован"
        response = self.dm_account_api.account_api.put_v1_account_email(json_data)
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        response = self.mail.mail_api.get_api_v2_messages()
        token = self.get_activation_token_by_login(login=login, response=response)
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        return response

    @staticmethod
    def get_activation_token_by_login(login, response):
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token