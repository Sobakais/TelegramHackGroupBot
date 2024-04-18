from aiogram import Router, F
from handlers.commands import nickname, menu, init_db

router = Router()
router.message.filter(F.text.startswith("!"))
router.include_routers(menu.router, init_db.router, nickname.router)
