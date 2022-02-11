import logging
from ubot.vars import Var
from telegram_upload import files
import time
import os
from ubot.plugins.progres import progress
import asyncio
from pyrogram.errors import FloodWait


async def send_vid(bot2, vid_path, chat_ix):
    try:
        atr = files.get_file_attributes(vid_path)
        duration = atr[0].duration
        width = atr[0].w
        height = atr[0].h
    except:
        if duration == None:
            duration = 0
        width = 1280
        height = 720
    try:
        filename_cmd = [
            "ffmpeg", "-i", f"{vid_path}", "-ss",
            f'{int(duration/2) if int(duration)<50 else "00:01:00"}',
            '-vframes', '1', f"{vid_path}.jpg"
        ]

        process = await asyncio.create_subprocess_exec(
            *filename_cmd,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        st1 = stderr.decode().strip()
        out1 = stdout.decode().strip()
        thumb = f"{vid_path}.jpg"

    except Exception as e:
        logging.info(e)

    logging.info(
        f"width >> {width} height >> {height} Duration >> {duration} file_path >> {vid_path} duration >> {duration} \n data >> {filename_cmd}"
    )
    if chat_ix != 0:
        chatID = chat_ix
    else:
        chatID = Var.CHANNEL_ID
    try:
        start_time1 = time.time()
        await bot2.send_video(
        chat_id=chatID,
        video=vid_path,
        width=width,
        height=height,
        duration=duration,
        supports_streaming=True,
        thumb=thumb,
        caption=vid_path.split("/")[-1],
        progress=progress,
        progress_args=(start_time1, f'Uploading {vid_path.split("/")[-1]}'))
    except FloodWait as e:
        await asyncio.sleep(e.x)
    await asyncio.sleep(5)

    try:
        os.remove(vid_path)

    except Exception as e:
        logging.info(e)
    try:
        os.remove(thumb)

    except Exception as e:
        logging.info(e)
