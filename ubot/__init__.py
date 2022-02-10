from sys import stderr, stdout
from pyrogram import Client, filters
import asyncio
import os
import time
from pyrogram.errors import FloodWait
import logging
from logging.handlers import RotatingFileHandler
from .bot2 import bot2
import base64
from .vars import Var

base64_bytes = Var.RCLONE_PASS.encode("utf-8")

sample_string_bytes = base64.b64decode(base64_bytes)
sample_string = sample_string_bytes.decode("utf-8")

f = open("rclone.conf", "w+", encoding="utf-8")
f.write(sample_string)
f.close()

logging.basicConfig(
    level=logging.DEBUG,
    format=
    "%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("Assist.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("aiohttp.web").setLevel(logging.WARNING)

LOGGER = logging.getLogger()
app = Client(session_name=Var.SESSION_STRING,
             api_hash=Var.API_HASH,
             api_id=Var.API_ID,
             device_model="Xiaomi pocof1",
             system_version="BifToGram 8.4.3")

channelDonor = []
rcloneFolder = []
offset_data = []
limitTele = []


class Timer:

    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False


timer = Timer()


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def progress(current, total, start, file):
    if timer.can_send():
        now = int(time.time())
        diff = now - start
        speed = current / diff
        LOGGER.info(
            f"{humanbytes(speed)}/S {current * 100 / total:.1f}% {file}")


@app.on_message(filters.user(Var.chat_Id) & filters.command("help"))
async def help(app, message):
    # LOGGER.info(message)

    await message.reply("Donor_Channel,Offset_id,Limit,Rclone_Folder")


@app.on_message(filters.user(Var.chat_Id) & filters.command("folder"))
async def folder(appd, message):
    raw_data = (message.reply_to_message.text).split(",")

    channelDonor.append(int(f"-100{(raw_data[0])}"))
    offset_data.append(int(raw_data[1]))
    limitTele.append(int(raw_data[2]))
    rcloneFolder.append(raw_data[3])

    await message.reply(
        f"{channelDonor[-1]},{offset_data[-1]},{limitTele[-1]},{rcloneFolder[-1]}"
    )


@app.on_message(filters.user(Var.chat_Id) & filters.command("copy"))
async def rclonev(appd, message):
    raw_data = (message.reply_to_message.text).split(",")
    rclonev = [
        "rclone", "--config", "rclone.conf", f"{raw_data[0]}",
        f"{raw_data[1]}", f"{raw_data[-1]}"
    ]
    rclonep = await asyncio.create_subprocess_exec(
        *rclonev,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    std, ste = await rclonep.communicate()
    LOGGER.info(std)
    LOGGER.info(ste)
    await message.reply(rclonep.returncode)


@app.on_message(filters.user(Var.chat_Id) & filters.command("rclonec"))
async def rclonec(appd, message):

    rclonec = ["rclone", "--config", "rclone.conf", "config"]
    rclonep1 = await asyncio.create_subprocess_exec(
        *rclonec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    std, ste = await rclonep1.communicate()
    LOGGER.info(std)
    LOGGER.info(ste)
    LOGGER.info(rclonep1.returncode)


@app.on_message(filters.user(Var.chat_Id) & filters.command("work"))
async def miror(appd, message):
    # LOGGER.info(type(channelDonor[-1]))
    #     LOGGER.info(rcloneFolder[-1])
    # LOGGER.info(filex)
    det = await app.get_history(int(channelDonor[-1]),
                                offset_id=int(offset_data[-1]),
                                limit=int(limitTele[-1]),
                                reverse=True)
    #     LOGGER.info(offset_data[-1])
    for deta in det:
        if deta.media == "video" or deta.media == "document":
            try:
                #             LOGGER.info(deta)
                if deta.media == "video":
                    filex = str(deta.message_id) + "_" + str(
                        deta.video.file_name)
                    if filex == "None":

                        filex = f"{str(deta.message_id)}_{int(time.time())}.mp4"
                if deta.media == "document":
                    filex = str(deta.message_id) + "_" + str(
                        deta.document.file_name)
                    if filex == "None":

                        filex = f"{str(deta.message_id)}_{int(time.time())}.pdf"
#             LOGGER.info(filex)

            except Exception as e:
                LOGGER.info(e)

            try:
                from os import path

                LOGGER.info(path.isdir("downloads"))
            except Exception as e:
                LOGGER.info(e)

#         LOGGER.info(rcloneFolder[-1])
            LOGGER.info(filex)
            start_time = time.time()
            try:
                try:
                    file_dir = await app.download_media(
                        deta,
                        file_name=f"./downloads/{filex}",
                        progress=progress,
                        progress_args=(start_time, filex))
                    if deta.caption:
                        caption = deta.caption
                    else:
                        caption = None
                    if deta.media == "video":
                        thumb = await app.download_media(
                            deta.video.thumbs[0].file_id)

                        if deta.video.width:
                            width = deta.video.width
                        else:
                            width = 0
                        if deta.video.height:
                            height = deta.video.height
                        else:
                            height = 0
                        if deta.video.duration:
                            duration = deta.video.duration
                        else:
                            duration = 0

                        start_time1 = time.time()
                        await bot2.send_video(
                            chat_id=Var.CHANNEL_ID,
                            video=file_dir,
                            width=width,
                            height=height,
                            duration=duration,
                            caption=caption,
                            thumb=thumb,
                            progress=progress,
                            progress_args=(
                                start_time1,
                                f'Uploading {file_dir.split("/")[-1]}'))
                    if deta.media == "document":
                        start_time2 = time.time()

                        await bot2.send_document(
                            chat_id=Var.CHANNEL_ID,
                            document=file_dir,
                            caption=caption,
                            force_document=True,
                            progress=progress,
                            progress_args=(
                                start_time2,
                                f'Uploading {file_dir.split("/")[-1]}'))

                    await asyncio.sleep(5)
                except Exception as e:
                    LOGGER.info(e)

            except FloodWait as e:
                LOGGER.info(f"Flood Wait Occured: {deta.message_id}")
                await asyncio.sleep(e.x)  # Wait "x" seconds before continuing
            filename_cmd = [
                "rclone", "--config", "rclone.conf", "move",
                f"./downloads/{filex}", f"{rcloneFolder[-1]}"
            ]
#             LOGGER.info(filename_cmd)
            process = await asyncio.create_subprocess_exec(
                *filename_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            await process.communicate()
            # LOGGER.info(stderr)
            # LOGGER.info(stdout)
            #             try:
            #                 if process.returncode == 0:
            #                     await message.reply(f"successfully uploaded > > {filex}")
            #                 else:
            #                     await message.reply(f"failed to upload > > {filex}")
            #             except:
            #                 pass

            LOGGER.info(process.returncode)
            try:
                os.remove(thumb)
            except:
                pass
    await message.reply("all done")


# @app.on_message(filters.user(Var.chat_Id) & filters.command("dir"))
# async def rcloneFoldere(app, message):
#     try:
#         path = "./downloads/"
#         arsd = os.listdir(path)
#         await message.reply(arsd)
#         path2 = "./"
#         arsd2 = os.listdir(path2)
#         await message.reply(arsd2)
#     except:
#         pass

# @app.on_message(filters.user(Var.chat_Id) & filters.command("purge"))
# async def purge(app, message):
#     path = "./downloads/"
#     LOGGER.info(path)
#     try:
#         shutil.rmtree(path)
#     except OSError:
#         await message.reply("Unable To Purge Your Files")


@app.on_message(filters.user(Var.chat_Id) & filters.command("logs"))
async def logss(app, message):
    arkeds = (os.path.isfile("Assist.txt"))
    await message.reply(arkeds)
    await message.reply_document(document="Assist.txt",
                                 caption="logs",
                                 quote=False)
