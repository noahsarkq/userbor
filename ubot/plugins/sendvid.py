import logging
from ubot.vars import Var
from telegram_upload import files
import subprocess
import time
import os
from ubot.plugins.progres import progress


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

        subprocess.run(
            data=
            f'ffmpeg -i "{vid_path}" -ss {int(duration/2) if duration!=0 else "00:01:00"} -vframes 1 "{vid_path}.jpg"',
            shell=True)
        thumb = f"{vid_path}.jpg"

    except:
        thumb = None
    if chat_ix != 0:
        chatID = chat_ix
    else:
        chatID = Var.CHANNEL_ID

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
    try:
        os.remove(vid_path)
        os.remove(thumb)
    except Exception as e:
        logging.info(e)
