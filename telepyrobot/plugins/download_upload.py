import asyncio
import math
import os
import time
import re
from datetime import datetime
from pySmartDL import SmartDL
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters, errors
from pyrogram.types import Message
import urllib.parse
from random import choice

import requests
from bs4 import BeautifulSoup
from pyDownload import Downloader

from telepyrobot import COMMAND_HAND_LER, LOGGER, TMP_DOWNLOAD_DIRECTORY
from telepyrobot.utils.dl_helpers import progress_for_pyrogram, humanbytes
from telepyrobot.utils.download_file import download_http
from telepyrobot.utils.check_if_thumb_exists import is_thumb_image_exists

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Download files using Telegram!

Syntax: `{COMMAND_HAND_LER}dl` / `{COMMAND_HAND_LER}download` <link> or as a reply to media
Use '|' along with command to set a custom filename for downloaded file,
Works only on replied media messages!

Upload Media to Telegram
Syntax: `{COMMAND_HAND_LER}upload <file>`

Upload files of a directory to Telegram
Usage: `{COMMAND_HAND_LER}batchup <directory>`

The command will upload all files from the directory location to the current Telegram Chat.
"""


@TelePyroBot.on_message(
    filters.command(["download", "dl"], COMMAND_HAND_LER) & filters.me
)
async def down_load_media(c: TelePyroBot, m: Message):
    sm = await m.reply_text("Checking...")
    if m.reply_to_message is not None:
        try:
            start_t = datetime.now()
            c_time = time.time()
            the_real_download_location = await c.download_media(
                message=m.reply_to_message,
                file_name=TMP_DOWNLOAD_DIRECTORY,
                progress=progress_for_pyrogram,
                progress_args=("**__Trying to download...__**", sm, c_time),
            )
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await sm.edit(
                f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds",
                parse_mode="html",
            )
        except Exception:
            exc = traceback.format_exc()
            await m.edit_text(f"Failed Download!\n{exc}")
            return
    elif len(m.command) > 1:
        try:
            await download_http(m, sm)
        except Exception:
            exc = traceback.format_exc()
            await m.edit_text(f"<b>Failed Download!</b>\n{exc}")
            return
    else:
        await sm.edit(
            "<code>Reply to a Telegram Media, to download it to local server.</code>"
        )
    await m.delete()
    return


@TelePyroBot.on_message(filters.command("upload", COMMAND_HAND_LER) & filters.me)
async def upload_as_document(c: TelePyroBot, m: Message):
    sm = await m.reply_text("`Uploading...`")
    if len(m.command) > 1:
        local_file_name = m.text.split(None, 1)[1]
        if os.path.exists(local_file_name):
            thumb_image_path = await is_thumb_image_exists(local_file_name)
            start_t = datetime.now()
            c_time = time.time()
            doc_caption = os.path.basename(local_file_name)
            await sm.edit_text(f"Uploading __{doc_caption}__...")
            await m.reply_document(
                document=local_file_name,
                thumb=thumb_image_path,
                caption=doc_caption,
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=m.message_id,
                progress=progress_for_pyrogram,
                progress_args=("Uploading file...", m, c_time),
            )
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await sm.delete()
            await m.reply_text(f"**Uploaded in {ms} seconds**")
        else:
            await sm.edit("404: media not found")
    else:
        await sm.edit(
            f"<code>{COMMAND_HAND_LER}upload FILE_PATH</code> to upload to current Telegram chat"
        )
    await m.delete()
    return


@TelePyroBot.on_message(filters.command("batchup", COMMAND_HAND_LER) & filters.me)
async def covid(c: TelePyroBot, m: Message):
    if len(m.text.split()) == 1:
        await m.edit_text("`Enter a directory location`")
    elif len(m.text.split()) >= 2:
        temp_dir = m.text.split(None, 1)[1]
        if not temp_dir.endswith("/"):
            temp_dir += "/"
    sm = await m.reply_text("`Uploading Files to Telegram...`")
    if os.path.exists(temp_dir):
        files = os.listdir(temp_dir)
        files.sort()
        total_files = len(files)
        file_no = 0
        for file in files:
            file_no += 1
            c_time = time.time()
            required_file_name = temp_dir + file
            thumb_image_path = await is_thumb_image_exists(required_file_name)
            doc_caption = os.path.basename(required_file_name)
            LOGGER.info(
                f"Uploading <i>{required_file_name}</i> from {temp_dir} to Telegram."
            )
            await c.send_document(
                chat_id=m.chat.id,
                document=required_file_name,
                thumb=thumb_image_path,
                caption=doc_caption,
                disable_notification=True,
                progress=progress_for_pyrogram,
                progress_args=(
                    f"Uploading file {file_no} of {total_files}\nFilename: <i>{file}</i>",
                    sm,
                    c_time,
                ),
            )
    else:
        await sm.edit("Directory Not Found.")
        return
    await sm.delete()
    await m.delete()
    await m.reply_text(f"Uploaded all files from Directory: <code>{temp_dir}</code>")
    LOGGER.info("Uploaded all files!")
    return
