# Импортируем escape, чтобы безопасно вставлять пользовательский текст в HTML.
from html import escape

# Импортируем F, чтобы отфильтровать текстовые сообщения.
from aiogram import F

# Импортируем Router, чтобы выделить обработчики перевода в отдельный роутер.
from aiogram import Router

# Импортируем Message, чтобы работать с сообщением пользователя.
from aiogram.types import Message

# Импортируем функцию перевода текста на английский язык.
from app.services.translator import translate_text_to_english


# Создаем роутер для перевода обычного текста.
router = Router()

# Создаем набор служебных кнопок, которые не нужно переводить.
SERVICE_BUTTONS = {"🚀 Старт", "ℹ️ Помощь", "🎤 Голос"}


# Ловим любые текстовые сообщения.
@router.message(F.text)
# Создаем обработчик перевода.
async def translate_handler(message: Message) -> None:
    # Убираем лишние пробелы по краям сообщения.
    user_text = message.text.strip()

    # Если после удаления пробелов текст пустой, просто выходим.
    if not user_text:
        # Завершаем работу обработчика без ответа.
        return

    # Если пользователь отправил команду, не трогаем ее в этом обработчике.
    if user_text.startswith("/"):
        # Завершаем работу обработчика без ответа.
        return

    # Если пользователь нажал служебную кнопку, не переводим ее как обычный текст.
    if user_text in SERVICE_BUTTONS:
        # Завершаем работу обработчика без ответа.
        return

    # Пробуем перевести текст на английский язык.
    try:
        # Получаем перевод.
        translated_text = await translate_text_to_english(user_text)

        # Отправляем пользователю красивый результат.
        await message.answer(
            text=(
                "🌍 <b>Перевод на английский готов</b>\n\n"
                f"📝 <b>Исходный текст:</b>\n<blockquote>{escape(user_text)}</blockquote>\n\n"
                f"🇬🇧 <b>Перевод:</b>\n<blockquote>{escape(translated_text)}</blockquote>"
            )
        )

    # Если сервис перевода временно не ответил, показываем понятное сообщение.
    except Exception:
        # Сообщаем пользователю о проблеме.
        await message.answer(
            "❌ Не удалось перевести текст прямо сейчас. "
            "Попробуй еще раз чуть позже."
        )