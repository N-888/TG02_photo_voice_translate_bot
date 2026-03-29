# Импортируем datetime, чтобы создавать уникальные имена файлов по времени.
from datetime import datetime

# Импортируем escape, чтобы безопасно показать путь в HTML-сообщении.
from html import escape

# Импортируем Bot, чтобы использовать у бота метод загрузки файла.
from aiogram import Bot

# Импортируем F, чтобы отфильтровать сообщения с фотографиями.
from aiogram import F

# Импортируем Router, чтобы оформить обработчик как отдельный роутер.
from aiogram import Router

# Импортируем Message, чтобы работать с входящим сообщением.
from aiogram.types import Message

# Импортируем настройки проекта, чтобы узнать путь к папке img.
from app.config import get_settings


# Создаем роутер для обработчиков фотографий.
router = Router()


# Ловим любое сообщение, в котором есть фотография.
@router.message(F.photo)
# Создаем обработчик сохранения фото.
async def save_photo_handler(message: Message, bot: Bot) -> None:
    # Получаем настройки проекта.
    settings = get_settings()

    # Берем самую большую версию фотографии из массива размеров.
    largest_photo = message.photo[-1]

    # Формируем уникальную временную метку.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # Формируем безопасное и уникальное имя файла.
    file_name = f"photo_{timestamp}_{largest_photo.file_unique_id}.jpg"

    # Формируем полный путь, куда будем сохранять изображение.
    destination_path = settings.images_dir / file_name

    # Пробуем скачать фото на диск.
    try:
        # Сохраняем фотографию в папку img.
        await bot.download(largest_photo, destination=destination_path)

        # Сообщаем пользователю, что все прошло успешно.
        await message.answer(
            text=(
                "✅ <b>Фото успешно сохранено</b>\n\n"
                f"📁 Папка: <code>{escape(str(settings.images_dir))}</code>\n"
                f"🖼 Имя файла: <code>{escape(destination_path.name)}</code>"
            )
        )

    # Если что-то пошло не так, не даем программе упасть и показываем понятный ответ.
    except Exception:
        # Сообщаем пользователю о проблеме.
        await message.answer(
            "❌ Не удалось сохранить фотографию. "
            "Проверь, что у программы есть доступ к папке проекта."
        )