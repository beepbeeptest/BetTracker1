import asyncio, os, logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
APP_URL   = os.getenv("APP_URL", "")   # https://your-app.railway.app

async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🎯 Открыть Bet Tracker", web_app={"url": APP_URL})
    ]])
    await message.answer(
        "Привет! Нажми кнопку, чтобы открыть трекер ставок 👇",
        reply_markup=kb
    )

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан")
    if not APP_URL:
        raise ValueError("APP_URL не задан")
    bot = Bot(token=BOT_TOKEN)
    dp  = Dispatcher(storage=MemoryStorage())
    dp.message.register(cmd_start, Command("start"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
