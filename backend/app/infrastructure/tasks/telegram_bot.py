from telegram import Bot

from app.core.config import settings


class TelegramNotifier:
    def __init__(self) -> None:
        self.bot = Bot(token=settings.telegram_token)

    async def send_notification(self, chat_id: str, message: str) -> None:
        await self.bot.send_message(chat_id=chat_id, text=message)
