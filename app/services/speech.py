# Импортируем asyncio, чтобы вынести синхронную озвучку в отдельный поток и не блокировать бота.
import asyncio

# Импортируем Path, чтобы удобно работать с временным файлом.
from pathlib import Path

# Импортируем NamedTemporaryFile, чтобы создать временный mp3-файл.
from tempfile import NamedTemporaryFile

# Импортируем FSInputFile, чтобы передать локальный файл в Telegram.
from aiogram.types import FSInputFile

# Импортируем gTTS, чтобы превращать текст в речь.
from gtts import gTTS


# Создаем синхронную функцию генерации mp3-файла с озвучкой текста.
def _create_mp3_speech_file(text: str) -> Path:
    # Создаем временный файл с расширением .mp3 и запрещаем его автоудаление до момента отправки.
    temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")

    # Превращаем путь временного файла в объект Path.
    temp_path = Path(temp_file.name)

    # Закрываем файл, чтобы Windows не мешал открыть его повторно на запись.
    temp_file.close()

    # Создаем объект озвучивания русского текста.
    tts = gTTS(text=text, lang="ru")

    # Сохраняем озвученный текст в наш временный mp3-файл.
    tts.save(str(temp_path))

    # Возвращаем путь к созданному файлу.
    return temp_path


# Создаем асинхронную функцию подготовки файла для отправки в Telegram.
async def create_voice_input_file(text: str) -> tuple[FSInputFile, Path]:
    # Генерируем mp3-файл в отдельном потоке, чтобы не зависал основной цикл бота.
    temp_path = await asyncio.to_thread(_create_mp3_speech_file, text)

    # Оборачиваем путь к файлу в формат, который понимает aiogram.
    voice_file = FSInputFile(path=temp_path)

    # Возвращаем и объект файла для отправки, и путь к нему для последующего удаления.
    return voice_file, temp_path


# Создаем функцию безопасного удаления временного файла.
def remove_file_safely(file_path: Path) -> None:
    # Проверяем, что файл действительно существует.
    if file_path.exists():
        # Удаляем временный файл с диска.
        file_path.unlink()