from clients.http.api_mail.apis.mail_api import MailApi
from packages.restclient.configuration import Configuration



class Mail_api:

    def __init__(self, configuration:Configuration):
        self.configuration = configuration
        self.mail_api = MailApi (configuration=self.configuration)
