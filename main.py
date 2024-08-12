from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from googletrans import Translator
import os
from config import API_TOKEN
import random

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
translator = Translator()

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который может сохранять фото, голосовые сообщения и переводить текст на английский.")

# Команда /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("/start - Приветственное сообщение\n/help - Описание команд\n/test - Случайная шутка\nПросто отправьте фото, голосовое сообщение или текст, и я обработаю их!")

# Команда /test
@dp.message_handler(commands=['test'])
async def send_test(message: types.Message):
    jokes = [
        "Почему программисты не любят природу? Слишком много багов.",
        "Какой лучший способ учить Python? Практиковаться на нем, пока не зазмеитесь!",
        "Что сказал Python другому коду? Ты вне цикла!"
    ]
    await message.reply(random.choice(jokes))

# Задача 1: Сохранение фото
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def save_photo(message: types.Message):
    photo = message.photo[-1]
    photo_path = f'img/{photo.file_id}.jpg'
    await photo.download(destination_file=photo_path)
    await message.reply("Фото сохранено!")

# Задача 2: Сохранение голосовых сообщений
@dp.message_handler(content_types=types.ContentType.VOICE)
async def receive_voice(message: types.Message):
    voice = message.voice
    await voice.download(destination_file=f'img/{voice.file_id}.ogg')
    await message.reply("Голосовое сообщение сохранено!")

# Задача 3: Перевод текста на английский
@dp.message_handler(lambda message: not message.text.startswith('/'))
async def translate_text(message: types.Message):
    translation = translator.translate(message.text, dest='en')
    await message.reply(f"Перевод: {translation.text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
