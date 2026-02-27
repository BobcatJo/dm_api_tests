from pathlib import Path
from telebot import TeleBot
from vyper import v
import telebot.apihelper as apihelper

config = Path(__file__).parent.joinpath('../../').joinpath('config')
v.set_config_name("prod")
v.add_config_path(config)
v.read_in_config()

apihelper.CONNECT_TIMEOUT = 30
apihelper.READ_TIMEOUT = 120

def send_file() -> None:
    telegram_bot = TeleBot(v.get("telegram.token"))
    file_path = Path(__file__).parent.joinpath('../../').joinpath("swagger-coverage-dm-api-account.html")
    with open(file_path, 'rb') as document:
        telegram_bot.send_document(
            v.get("telegram.chat_id"),
            document=document,
            caption="coverage",
            )


if __name__ == "__main__":
    send_file()