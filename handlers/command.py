from aiogram import Router, F
from handlers.commands import nickname, menu

router = Router()
router.message.filter(F.text.startswith("!"))
router.include_routers(menu.router, nickname.router)
