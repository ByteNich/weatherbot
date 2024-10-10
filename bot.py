import asyncio
from imaplib import Commands
import logging
import sys
from os import getenv
from dotenv import load_dotenv

import requests

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

load_dotenv()

TOKEN = getenv("TELEGRAM_BOT_TOKEN")
TOKEN_API_WEATHER = getenv("WEATHER_API_TOKEN")
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!\nВведи /w название города , чтобы узнать погоду\nПример: /w Москва")


@dp.message(Command(commands='weather'))
async def weather_answer(message:Message,
                        command: CommandObject
                        ):
    asrgs = command.args
    try:
        r = requests.get(f"http://api.weatherapi.com/v1/current.json?key={TOKEN_API_WEATHER}&q={asrgs}").json()
        city = r['location']['name']
        temp_c = r['current']['temp_c']
        await message.answer(f'В городе {city} сейчас {temp_c}°C')
    except:
        await message.answer('Введёный город не найден')


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())