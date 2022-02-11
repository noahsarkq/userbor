from ubot.vars import Var
from telegram_upload import files

import time

from ubot.plugins.progres import progress


async def send_vid(bot2, vid_path, chat_ix):
    try:
        atr = files.get_file_attributes(vid_path)
        duration = atr[0].duration
        width = atr[0].w
        height = atr[0].h
    except:
        duration = 0
        width = 1280
        height = 720
    try:

        thumb = files.get_video_thumb(vid_path, None, width)

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
        caption=vid_path.split("/")[-1],
        progress=progress,
        progress_args=(start_time1, f'Uploading {vid_path.split("/")[-1]}'))
