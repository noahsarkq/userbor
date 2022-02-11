from pyrogram import Client, filters
from .vars import Var
from pyrogram.types import Message
import asyncio
from pyrogram.errors import FloodWait
from ubot.detail import *
from ubot.plugins.sendvid import send_vid
import os
bot2 = Client("bot2",
              api_hash=Var.API_HASH,
              api_id=Var.API_ID,
              bot_token=Var.BOT_TOKEN)

stopCopy = [0]
chat_ix = [0]
breaker=[0]

@bot2.on_message(filters.user(Var.chat_Id) & filters.command("help"))
async def help(_, m: Message):
    await m.reply("from_chatID, to_chatId, num1, num2 \n \n To stop Copy '1'")


@bot2.on_message(filters.user(Var.chat_Id) & filters.command("chatid"))
async def help(_, m: Message):
    chat_ix.append(int(m.reply_to_message.text))
    await m.reply(chat_ix[-1])
@bot2.on_message(filters.user(Var.chat_Id) & filters.command("break"))
async def help(_, m: Message):
    breaker.append(int(m.reply_to_message.text))
    await m.reply(breaker[-1])

@bot2.on_message(filters.user(Var.chat_Id) & filters.command("stcopy"))
async def stop_copy(_, m: Message):
    if int(m.reply_to_message.text) == 1:
        stopCopy.append(int(m.reply_to_message.text))


@bot2.on_message(filters.user(Var.chat_Id) & filters.command("copy"))
async def copy_messages(_, m: Message):
    if "," in m.reply_to_message.text:
        from_chatID, to_chatId, num1, num2 = m.reply_to_message.text.split(",")
        for message_id in range(int(num1), int(num2) + 1):
            if stopCopy[-1] == 1:
                await m.reply(f"Copied Till {message_id-1}")
                break
            try:
                await bot2.copy_message(chat_id=int(f"-100{to_chatId}"),
                                        from_chat_id=int(f"-100{from_chatID}"),
                                        message_id=message_id)
                await asyncio.sleep(4)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await m.reply(f"Flood wait Occured for {e.x}")
                pass
        await m.reply("All Copied")


@bot2.on_message(filters.chat(Var.chat_Id) & filters.command("txtdl"))
async def txtdl(_, m: Message):
    msg=m.reply_to_message
    
   # msg = await bot2.get_messages(msg.chat.id, msg.message_id)
    #print(msg)
    
    if msg.document is not None:
        x= await msg.download()
        

        

        try:    
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            list_data = []
            
            for i in content:
  
                list_data.append(i)
            os.remove(x)
            # print(len(links))
        except:
            await m.reply_text("Invalid file input.")
            os.remove(x)
            return
    elif m.reply_to_message.text is not None:
        list_data = m.reply_to_message.text.split("\n")
    else: 
        return
        
        
    for psdata in list_data:
        if breaker[-1]==1:
            break

        if "," in psdata:
            file_path, link = psdata.split(",")
            file_name = await filenamegen(link, file_path)
        else:
            file_name = await filenamegen(psdata)
            link = psdata
        file_path = f"./downloads/{file_name}"
        await yt_dl(file_path, link)
        
        await send_vid(bot2, file_path, chat_ix[-1])
        #await m.reply(f"Success fully uploaded {file_name}")
