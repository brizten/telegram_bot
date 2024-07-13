import asyncio
import logging
import sys

import keyring

from asteroid import detector

from aiocron import crontab
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = keyring.get_password('telega', 'api')
CHAT_ID = keyring.get_password('telega', 'chat_id')  # Replace with the chat ID you want to send the message to

# Initialize the Dispatcher
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer('hello my lord')


async def send_asteroid_info(bot: Bot) -> None:
    """
    Sends a message to the chat every minute
    """
    asteroid_info = detector()
    await bot.send_message(chat_id=CHAT_ID, text=asteroid_info)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    crontab('0 9 * * *', func=send_asteroid_info, args=[bot], start=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
