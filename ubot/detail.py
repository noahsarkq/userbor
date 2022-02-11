from subprocess import *
from ubot import logging
import asyncio


async def filenamegen(link: str, file_name: str = None):
    filename_cmd = [
        "yt-dlp", "--skip-download", "--youtube-skip-dash-manifest",
        "--get-filename", "--restrict-filenames", "--no-check-certificate",
        "--no-warning", "-o",
        f'"{file_name if file_name else "%(title)s"}.%(ext)s"', link
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
    # logging.info(stdout)
    # logging.info("--------------------")
    # logging.info(stderr)
    logging.info(out1[1:-1])
    return out1[1:-1]


async def yt_dl(vid_path, link):

    filename_cmd = [
        "yt-dlp", "-o", vid_path, "-R", "25", "--youtube-skip-dash-manifest",
        "--fragment-retries", "25", "--no-check-certificate",
        "--external-downloader", "aria2c", "--downloader-args",
        "aria2c: -s 8 -x 8 -j 32 -k 5M", link
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
    # logging.info(st1)
    # logging.info("---------------------")
    # logging.info(out1)
    # logging.info("---------------------")

    logging.info(process.returncode)
