# Импортируем escape, чтобы безопасно вставлять имя пользователя в HTML-текст.
from html import escape

# Импортируем F, чтобы удобно фильтровать текст кнопок.
from aiogram import F

# Импортируем Router, чтобы оформить этот набор обработчиков отдельным модулем.
from aiogram import Router

# Импортируем Command, чтобы обрабатывать обычные команды вроде /help.
from aiogram.filters import Command

# Импортируем CommandStart, чтобы красиво обработать команду /start.
from aiogram.filters import CommandStart

# Импортируем Message, чтобы работать с входящими сообщениями.
from aiogram.types import Message

# Импортируем функцию создания нижней клавиатуры.
from app.keyboards.main_menu import get_main_menu


# Создаем роутер для этого файла.
router = Router()


# Обрабатываем команду /start.
@router.message(CommandStart())
# Обрабатываем нажатие кнопки "Старт".
@router.message(F.text == "🚀 Старт")
# Создаем обработчик стартового сообщения.
async def start_handler(message: Message) -> None:
    # Получаем имя пользователя, если Telegram его передал.
    first_name = message.from_user.first_name if message.from_user else "друг"

    # Отправляем красивое приветствие и показываем клавиатуру.
    await message.answer(
        text=(
            f"👋 <b>Привет, {escape(first_name)}!</b>\n\n"
            "Я современный учебный бот и умею:\n"
            "• сохранять твои фото в папку <code>img</code>\n"
            "• отправлять голосовое сообщение\n"
            "• переводить любой твой обычный текст на английский язык\n\n"
            "👇 Нажми кнопку ниже или просто отправь мне сообщение."
        ),
        reply_markup=get_main_menu(),
    )


# Обрабатываем команду /help.
@router.message(Command("help"))
# Обрабатываем нажатие кнопки "Помощь".
@router.message(F.text == "ℹ️ Помощь")
# Создаем обработчик справки.
async def help_handler(message: Message) -> None:
    # Отправляем подробную справку по возможностям бота.
    await message.answer(
        text=(
            "ℹ️ <b>Справка по боту</b>\n\n"
            "<b>Что умеет бот:</b>\n"
            "1. Любое фото, которое ты отправишь, бот сохранит в папку <code>img</code>.\n"
            "2. Команда <code>/voice</code> или кнопка <b>🎤 Голос</b> отправит голосовое сообщение.\n"
            "3. Любой обычный текст бот переведет на английский язык.\n\n"
            "<b>Команды:</b>\n"
            "• <code>/start</code> — приветствие\n"
            "• <code>/help</code> — помощь\n"
            "• <code>/voice</code> — голосовое сообщение\n\n"
            "🖼 Просто отправь фото.\n"
            "🌍 Просто отправь текст."
        ),
        reply_markup=get_main_menu(),
    )