# Импортируем F, чтобы реагировать на текст кнопки.
from aiogram import F

# Импортируем Router, чтобы оформить этот обработчик отдельно.
from aiogram import Router

# Импортируем Command, чтобы обработать команду /voice.
from aiogram.filters import Command

# Импортируем Message, чтобы работать с входящим сообщением.
from aiogram.types import Message

# Импортируем настройки проекта, чтобы взять текст для озвучивания.
from app.config import get_settings

# Импортируем функцию создания временного голосового файла.
from app.services.speech import create_voice_input_file

# Импортируем функцию безопасного удаления временного файла.
from app.services.speech import remove_file_safely


# Создаем роутер для голосового сообщения.
router = Router()


# Обрабатываем команду /voice.
@router.message(Command("voice"))
# Обрабатываем нажатие кнопки "Голос".
@router.message(F.text == "🎤 Голос")
# Создаем обработчик отправки голосового сообщения.
async def voice_handler(message: Message) -> None:
    # Получаем настройки проекта.
    settings = get_settings()

    # Сразу создаем переменную для пути к временному файлу.
    temp_path = None

    # Пробуем создать и отправить голосовое сообщение.
    try:
        # Сообщаем пользователю, что бот начал подготовку голоса.
        await message.answer("⏳ Готовлю голосовое сообщение...")

        # Создаем голосовой файл и получаем путь к нему.
        voice_file, temp_path = await create_voice_input_file(settings.voice_text)

        # Отправляем готовое голосовое сообщение пользователю.
        await message.answer_voice(
            voice=voice_file,
            caption="🎤 <b>Готово!</b> Это голосовое сообщение от бота.",
        )

    # Если озвучивание не получилось, перехватываем ошибку и показываем мягкий ответ.
    except Exception:
        # Сообщаем пользователю о проблеме.
        await message.answer(
            "❌ Не удалось создать голосовое сообщение. "
            "Проверь интернет-соединение и попробуй еще раз."
        )

    # Этот блок выполнится в любом случае: и после успеха, и после ошибки.
    finally:
        # Проверяем, что временный файл действительно был создан.
        if temp_path is not None:
            # Удаляем временный файл после отправки.
            remove_file_safely(temp_path)