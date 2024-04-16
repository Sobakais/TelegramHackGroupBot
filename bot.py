import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, command, all_text
from handlers.commands.hack_menu import fsm_callback
from handlers.commands.hack_menu import show_hacks as csh
from handlers.commands.hack_menu import delete_hack
from resources import config as cfg

bot = Bot(token=cfg.BOT_TOKEN)


async def main():
    dp = Dispatcher()
    # Запуск бота

    dp.include_routers(
        fsm_callback.router,
        csh.router,
        delete_hack.router,
        start.router,
        command.router,
        all_text.router,
    )
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
