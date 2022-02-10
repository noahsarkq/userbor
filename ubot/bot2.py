from pyrogram import Client, filters
from .vars import Var

bot2 = Client("bot2",
              api_hash=Var.API_HASH,
              api_id=Var.API_ID,
              bot_token=Var.BOT_TOKEN)


@bot2.on_message(filters.user(Var.chat_Id))
async def help(_, message):
    await message.reply("yes")