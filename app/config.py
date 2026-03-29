# Импортируем dataclass, чтобы удобно хранить настройки проекта в одном объекте.
from dataclasses import dataclass

# Импортируем Path, чтобы удобно работать с путями к папкам и файлам.
from pathlib import Path

# Импортируем os, чтобы получать переменные окружения из .env.
import os

# Импортируем load_dotenv, чтобы загружать данные из файла .env.
from dotenv import load_dotenv


# Получаем путь к папке, в которой лежит текущий файл config.py.
APP_DIR = Path(__file__).resolve().parent

# Получаем путь к корню проекта.
BASE_DIR = APP_DIR.parent

# Загружаем значения из файла .env, который лежит в корне проекта.
load_dotenv(BASE_DIR / ".env")


# Создаем неизменяемый класс настроек проекта.
@dataclass(frozen=True)
class Settings:
    # Сохраняем токен Telegram-бота.
    bot_token: str

    # Сохраняем путь к папке, в которую будут складываться фотографии.
    images_dir: Path

    # Сохраняем текст, который будет озвучиваться в голосовом сообщении.
    voice_text: str


# Создаем функцию, которая собирает и проверяет все настройки проекта.
def get_settings() -> Settings:
    # Получаем токен из переменной окружения BOT_TOKEN.
    bot_token = os.getenv("BOT_TOKEN", "").strip()

    # Получаем текст для голосового сообщения из переменной окружения VOICE_TEXT.
    voice_text = os.getenv(
        "VOICE_TEXT",
        "Привет! Я отправляю тебе голосовое сообщение.",
    ).strip()

    # Формируем путь к папке img в корне проекта.
    images_dir = BASE_DIR / "img"

    # Создаем папку img автоматически, если ее еще нет.
    images_dir.mkdir(parents=True, exist_ok=True)

    # Проверяем, что токен действительно заполнен.
    if not bot_token:
        # Вызываем понятную ошибку, если токен не был вставлен в .env.
        raise ValueError(
            "В файле .env не найден BOT_TOKEN. "
            "Открой файл .env и вставь туда токен от BotFather."
        )

    # Возвращаем готовый объект со всеми настройками проекта.
    return Settings(
        bot_token=bot_token,
        images_dir=images_dir,
        voice_text=voice_text,
    )