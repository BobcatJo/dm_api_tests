import requests

from restclient.client import RestClient
class AccountApi(RestClient):



    def post_v1_account(self,json_data):
        response = self.post(path=f'/v1/account', json=json_data)
        return response

        """
        Register new user
        :param json_data:
        :return:
        """


    def put_v1_account_token(self,token):
        headers = {'accept': 'text/plain', }
        response = self.put(path=f'/v1/account/{token}',headers=headers)
        return response

        """
        Activate register user
        :param token:
        :return:
        """

    def put_v1_account_email(self, json_data):
        response = self.put(path=f'/v1/account/email',json=json_data)
        return response

        """
        Change registered user email
        :param json_data:
        :return
        """