# Импортируем asyncio, чтобы выполнять перевод в отдельном потоке и не подвешивать бота.
import asyncio

# Импортируем GoogleTranslator из deep-translator для перевода текста на английский язык.
from deep_translator import GoogleTranslator


# Создаем синхронную функцию перевода текста.
def _translate_sync(text: str) -> str:
    # Создаем объект переводчика с автоопределением исходного языка и переводом в английский.
    translator = GoogleTranslator(source="auto", target="en")

    # Выполняем перевод текста.
    translated_text = translator.translate(text)

    # Возвращаем готовый перевод.
    return translated_text


# Создаем асинхронную функцию, которую будем вызывать из обработчика сообщений.
async def translate_text_to_english(text: str) -> str:
    # Выносим синхронный перевод в отдельный поток, чтобы основной цикл бота не блокировался.
    translated_text = await asyncio.to_thread(_translate_sync, text)

    # Возвращаем результат перевода.
    return translated_text