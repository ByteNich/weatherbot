import asyncio
import logging
import sys
from os import getenv

import requests
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TELEGRAM_BOT_TOKEN")
TOKEN_API_WEATHER = getenv("WEATHER_API_TOKEN")
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\nВведи /weather название города , чтобы узнать погоду\nПример: /weather Москва"
    )


@dp.message(Command(commands="weather"))
async def weather_answer(message: Message, command: CommandObject):
    asrgs = command.args
    try:
        r = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key={TOKEN_API_WEATHER}&q={asrgs}&lang=ru"
        ).json()
        city = r["location"]["name"]
        time_local = r["location"]["localtime"].split()[1]
        condition = r["current"]["condition"]["text"]
        temp_c = r["current"]["temp_c"]
        wind_kph = r["current"]["wind_kph"]

        await message.answer(
            f"В городе {city} сейчас {temp_c}°C\nМестное время {time_local}\n{condition}\nСкорость ветра {wind_kph} км/ч"
        )
    except:  # noqa: E722
        await message.answer("Введёный город не найден")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
