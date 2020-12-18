import asyncio
import math
import os
import shutil
import urllib.parse
import time
from datetime import datetime
from pySmartDL import SmartDL
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters, errors
from pyrogram.types import Message
from pyDownload import Downloader
from telepyrobot import LOGGER, TMP_DOWNLOAD_DIRECTORY
from telepyrobot.utils.dl_helpers import humanbytes


async def download_http(m, status_message):
    start_t = datetime.now()
    the_url_parts = " ".join(m.command[1:])
    url = the_url_parts.strip()
    custom_file_name = os.path.basename(url)
    if "|" in the_url_parts:
        url, custom_file_name = the_url_parts.split("|")
        url = url.strip()
        custom_file_name = custom_file_name.strip()
    download_file_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, custom_file_name)
    downloader = SmartDL(url, download_file_path, progress_bar=False)
    downloader.start(blocking=False)
    c_time = time.time()
    while not downloader.isFinished():
        total_length = downloader.filesize if downloader.filesize else None
        downloaded = downloader.get_dl_size()
        display_message = ""
        now = time.time()
        diff = now - c_time
        percentage = downloader.get_progress() * 100
        speed = downloader.get_speed(human=True)
        elapsed_time = round(diff) * 1000
        progress_str = "**[{0}{1}]**\n**Progress:** __{2}%__".format(
            "".join(["●" for i in range(math.floor(percentage / 5))]),
            "".join(["○" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )
        estimated_total_time = downloader.get_eta(human=True)
        try:
            current_message = f"__**Trying to download...**__\n"
            current_message += f"**URL:** `{url}`\n"
            current_message += (
                f"**File Name:** `{urllib.parse.unquote(custom_file_name)}`\n"
            )
            current_message += f"{progress_str}\n"
            current_message += (
                f"__{humanbytes(downloaded)} of {humanbytes(total_length)}__\n"
            )
            current_message += f"**Speed:** __{speed}__\n"
            current_message += f"**ETA:** __{estimated_total_time}__"
            if round(diff % 10.00) == 0 and current_message != display_message:
                await status_message.edit(
                    disable_web_page_preview=True, text=current_message
                )
                display_message = current_message
                await asyncio.sleep(10)
        except errors.MessageNotModified:  # Don't log error if Message is not modified
            pass
        except Exception as e:
            LOGGER.info(str(e))
            pass
    if os.path.exists(download_file_path):
        new_file_name = urllib.parse.unquote(download_file_path)
        shutil.move(download_file_path, new_file_name)
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await status_message.edit(
            f"Downloaded to <code>{new_file_name}</code> in <u>{ms}</u> seconds.\nDownload Speed: {humanbytes(total_length)}/s",
            parse_mode="html",
        )
        return new_file_name