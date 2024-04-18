from pyrogram import Client
from resources import config

api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN


async def get_chat_members(chat_id):
    app = Client(
        "my_bot",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        in_memory=True,
    )
    await app.start()
    members = []
    async for member in app.get_chat_members(chat_id):
        if member.user.id == config.bot_tg_id:
            continue
        members.append([member.user.id, member.user.username])
    await app.stop()

    return members
