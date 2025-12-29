import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from tiktok import get_tiktok_video

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://your-app.onrender.com/webhook

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    url = message.text.strip()

    if "tiktok.com" not in url:
        await message.answer("Отправь ссылку на TikTok")
        return

    await message.answer("Скачиваю...")

    video_url = await get_tiktok_video(url)

    if not video_url:
        await message.answer("Не удалось скачать видео")
        return

    await message.answer_video(video_url)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()

def main():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dp, bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

if __name__ == "__main__":
    main()