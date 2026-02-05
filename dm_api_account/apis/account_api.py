import requests


class AccountApi:

    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account(
            self,
            json_data
    ):
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )
        """
        Register new user
        :param json_data:
        :return
        """
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate register user
        :param token:
        :return:
        """

        response = requests.put(
            url=f'{self.host}/v1/account/{token}'
        )
        return response
