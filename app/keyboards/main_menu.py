# Импортируем KeyboardButton, чтобы создать кнопки на клавиатуре Telegram.
from aiogram.types import KeyboardButton

# Импортируем ReplyKeyboardMarkup, чтобы собрать кнопки в нижнюю клавиатуру.
from aiogram.types import ReplyKeyboardMarkup


# Создаем функцию, которая возвращает главную клавиатуру бота.
def get_main_menu() -> ReplyKeyboardMarkup:
    # Возвращаем готовую клавиатуру с красивыми кнопками.
    return ReplyKeyboardMarkup(
        # Описываем строки кнопок на клавиатуре.
        keyboard=[
            [
                KeyboardButton(text="🚀 Старт"),
                KeyboardButton(text="ℹ️ Помощь"),
            ],
            [
                KeyboardButton(text="🎤 Голос"),
            ],
        ],
        # Включаем автоуменьшение клавиатуры, чтобы она выглядела аккуратнее.
        resize_keyboard=True,
        # Добавляем подсказку в поле ввода.
        input_field_placeholder="Напиши текст для перевода или отправь фото",
    )