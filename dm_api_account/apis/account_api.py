import requests


class AccountApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

        """
        Register new user
        :param json_data:
        :return:
        """

    def post_v1_account(self,json_data):
        response = requests.post(url=f'{self.host}/v1/account', json=json_data)
        return response

        """
        Activate register user
        :param token:
        :return:
        """

    def put_v1_account_token(self,token):
        headers = {'accept': 'text/plain', }
        response = requests.put(url=f'{self.host}/v1/account/{token}',headers=headers)
        return response

    def put_v1_account_email(self, json_data):
        """
       Change registered user email
       :param json_data:
       :return
       """

        response = requests.put(url=f'{self.host}/v1/account/email',json=json_data)
        return response
