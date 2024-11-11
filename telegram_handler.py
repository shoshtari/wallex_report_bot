import telegram
import asyncio


class TelegramHandler:
    def __init__(self, bot_token: str, chat_id: str, base_url="https://api.telegram.org"):
        self.__bot = telegram.Bot(bot_token)
        self.__chat_id = chat_id

    async def send_message(self, text):
        await self.__bot.send_message(chat_id=chat_id, text=text)

    async def edit_message(self, message_id, text):
        await self.__bot.edit_message_text(
            text=text, message_id=message_id, chat_id=self.__chat_id)
