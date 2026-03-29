# Импортируем Dispatcher, чтобы подключить к нему все роутеры.
from aiogram import Dispatcher

# Импортируем роутер стартовых и справочных сообщений.
from app.handlers.start_help import router as start_help_router

# Импортируем роутер для сохранения фотографий.
from app.handlers.photos import router as photos_router

# Импортируем роутер для голосового сообщения.
from app.handlers.voice import router as voice_router

# Импортируем роутер для перевода текста.
from app.handlers.translate import router as translate_router


# Создаем функцию регистрации всех роутеров проекта.
def register_routers(dp: Dispatcher) -> None:
    # Подключаем роутер со стартом и помощью.
    dp.include_router(start_help_router)

    # Подключаем роутер с голосовым сообщением.
    dp.include_router(voice_router)

    # Подключаем роутер для сохранения фото.
    dp.include_router(photos_router)

    # Подключаем роутер для перевода обычного текста.
    dp.include_router(translate_router)