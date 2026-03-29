# Импортируем asyncio, чтобы запустить асинхронную точку входа.
import asyncio

# Импортируем logging, чтобы видеть служебные сообщения в консоли.
import logging

# Импортируем sys, чтобы направить логи в стандартный вывод PyCharm.
import sys

# Импортируем Bot, чтобы создать объект Telegram-бота.
from aiogram import Bot

# Импортируем Dispatcher, чтобы принимать и распределять обновления от Telegram.
from aiogram import Dispatcher

# Импортируем DefaultBotProperties, чтобы задать общие свойства для сообщений бота.
from aiogram.client.default import DefaultBotProperties

# Импортируем ParseMode, чтобы бот умел отправлять красиво оформленный HTML-текст.
from aiogram.enums import ParseMode

# Импортируем функцию получения настроек проекта из файла .env.
from app.config import get_settings

# Импортируем функцию подключения всех обработчиков.
from app.handlers import register_routers


# Создаем главную асинхронную функцию запуска бота.
async def main() -> None:
    # Включаем логирование уровня INFO, чтобы видеть запуск, ошибки и входящие события.
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Читаем настройки проекта из файла .env.
    settings = get_settings()

    # Создаем диспетчер, который будет направлять входящие сообщения в нужные обработчики.
    dp = Dispatcher()

    # Подключаем все роутеры проекта.
    register_routers(dp)

    # Открываем соединение с Telegram от имени нашего бота.
    async with Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    ) as bot:
        # Запускаем long polling, чтобы бот начал получать новые сообщения.
        await dp.start_polling(bot)


# Проверяем, что файл запущен напрямую, а не импортирован из другого модуля.
if __name__ == "__main__":
    # Запускаем главную асинхронную функцию.
    asyncio.run(main())