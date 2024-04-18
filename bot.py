import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, command, all_text, voice_messages
from handlers.commands.hack_menu import show_hacks, delete_hack, add_hack, edit_hack
from resources import config as cfg


async def main():
    bot = Bot(token=cfg.BOT_TOKEN)
    dp = Dispatcher()
    # Запуск бота

    dp.include_routers(
        add_hack.router,
        # edit_hack.router,
        show_hacks.router,
        delete_hack.router,
        start.router,
        command.router,
        voice_messages.router,
        all_text.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
