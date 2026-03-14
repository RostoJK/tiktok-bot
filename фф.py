import asyncio
import re
import os
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from yt_dlp import YoutubeDL

TOKEN = "8629550597:AAEqxvL-mIXQbmdxVc-5MvRrHlOGZXJI2-Y"

bot = Bot(TOKEN)
dp = Dispatcher()


# Проверка ссылки
def validate_url(url: str):
    yt = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"
    tt = r"(https?://)?(www\.)?(tiktok\.com)/"
    return re.match(yt, url) or re.match(tt, url)


# Скачивание видео
async def download_video(url: str, filename: str):
    ydl_opts = {
        "outtmpl": filename,
        "format": "mp4/best",
        "quiet": True,
        "noprogress": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# Извлечение аудио через FFmpeg
def extract_audio(video_path: str, audio_path: str):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "mp3",
        audio_path,
        "-y"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Отправь ссылку на TikTok или YouTube, я скачаю видео и MP3.")


@dp.message()
async def handle(message: types.Message):
    url = message.text.strip()

    if not validate_url(url):
        await message.answer("Отправь корректную ссылку на TikTok или YouTube.")
        return

    await message.answer("Скачиваю...")

    video_path = "video.mp4"
    audio_path = "audio.mp3"

    try:
        # Скачиваем видео
        await download_video(url, video_path)

        # Извлекаем аудио
        extract_audio(video_path, audio_path)

        # Готовим файлы для отправки
        video = FSInputFile(video_path)
        audio = FSInputFile(audio_path)

        # Отправляем видео
        await message.answer_video(video)

        # Отправляем аудио
        await message.answer_audio(audio)

    except Exception as e:
        await message.answer(f"Ошибка: {e}")

    finally:
        # Удаляем временные файлы
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())