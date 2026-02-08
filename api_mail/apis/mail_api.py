import requests


class MailApi:

    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers

        """
        Get users emails
        :return:
        """

    def get_api_v2_messages(
            self,
            limit=50
    ):
        params = {
            'limit': limit,
        }
        response = requests.get(
            url=f'{self.host}/api/v2/messages',
            params=params,
            verify=False
        )
        return response
