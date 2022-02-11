from pyrogram import Client, filters
from .vars import Var
from pyrogram.types import Message
import asyncio
from pyrogram.errors import FloodWait

bot2 = Client("bot2",
              api_hash=Var.API_HASH,
              api_id=Var.API_ID,
              bot_token=Var.BOT_TOKEN)


@bot2.on_message(filters.user(Var.chat_Id) & filters.command("help"))
async def help(_, message):
    await message.reply("from_chatID, to_chatId, num1, num2")


@bot2.on_message(filters.user(Var.chat_Id) & filters.command("copy"))
async def copy_messages(_, m: Message):
    from_chatID, to_chatId, num1, num2 = m.reply_to_message.text.split(",")
    for message_id in range(int(num1), int(num2) + 1):
        try:
            await bot2.copy_message(chat_id=int(to_chatId),
                                    from_chat_id=int(from_chatID),
                                    message_id=message_id)
            await asyncio.sleep(4)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            pass