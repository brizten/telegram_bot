import asyncio
import logging
import sys
import keyring
from asteroid import detector
from weather import get_weather
from aiocron import crontab
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = keyring.get_password('telega', 'api')
CHAT_ID = keyring.get_password('telega', 'chat_id')

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

@dp.message(Command("asteroid"))
async def send_asteroid_info(message: Message) -> None:
    """
    Sends a message to the chat every minute
    """
    asteroid_info = detector()
    await message.answer(asteroid_info)


async def send_weather_info(bot: Bot) -> None:
    """
    Sends weather information
    """
    weather_info = get_weather()
    await bot.send_message(chat_id=CHAT_ID, text=weather_info)


@dp.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    """
    Sends weather info in response to the "погода" command
    """
    weather_info = get_weather()
    await message.answer(weather_info)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Запускаем крон-задачи
    crontab('0 9 * * *', func=send_asteroid_info, args=[bot], start=True)
    crontab('0 9 * * *', func=send_weather_info, args=[bot], start=True)

    # Стартуем диспетчер
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
