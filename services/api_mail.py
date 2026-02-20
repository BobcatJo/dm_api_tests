from restclient.configuration import Configuration
from api_mail.apis.mail_api import MailApi


class Mail_api:

    def __init__(self, configuration:Configuration):
        self.configuration = configuration
        self.mail_api = MailApi (configuration=self.configuration)
