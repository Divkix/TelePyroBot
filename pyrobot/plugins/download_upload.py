import asyncio
import math
import os
import time
from datetime import datetime
from pySmartDL import SmartDL
from pyrogram import Client, Filters
import json
import logging
import re
import urllib.parse
from random import choice

import requests
from bs4 import BeautifulSoup
from pyDownload import Downloader

from pyrobot import COMMAND_HAND_LER, LOGGER, TMP_DOWNLOAD_DIRECTORY
from pyrobot.utils.display_progress_dl_up import (
    progress_for_pyrogram,
    humanbytes
)
from pyrobot.utils.check_if_thumb_exists import is_thumb_image_exists

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Download Telegram Media
Syntax: `{COMMAND_HAND_LER}dl` / download <link> or as a reply to media
Use '|' along with command to set a custom filename fro downloaded file,
Works only on replied media messages!

Upload Media to Telegram
Syntax: `{COMMAND_HAND_LER}upload <file location>`

Upload files of a directory to Telegram
Usage: `{COMMAND_HAND_LER}batchup <directory location>`

The command will upload all files from the directory location to the current Telegram Chat.
"""


@Client.on_message(Filters.command(["download", "dl"], COMMAND_HAND_LER) & Filters.me)
async def down_load_media(client, sms):
    message = await sms.reply_text("...", quote=True)
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    if sms.reply_to_message is not None:
        start_t = datetime.now()
        download_location = TMP_DOWNLOAD_DIRECTORY + "/"
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=sms.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                "**__Trying to download...__**", message, c_time
            )
        )
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await message.edit(f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds", parse_mode="html")
        await sms.delete()
    elif len(sms.command) > 1:
        start_t = datetime.now()
        the_url_parts = " ".join(sms.command[1:])
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
                ''.join(["●" for i in range(math.floor(percentage / 5))]),
                ''.join(["○" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"__**Trying to download...**__\n"
                current_message += f"**URL:** `{url}`\n"
                current_message += f"**File Name:** `{custom_file_name}`\n"
                current_message += f"{progress_str}\n"
                current_message += f"__{humanbytes(downloaded)} of {humanbytes(total_length)}__\n"
                current_message += f"**Download Speed** __{speed}__\n"
                current_message += f"**ETA:** __{estimated_total_time}__"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await message.edit(
                        disable_web_page_preview=True,
                        text=current_message
                    )
                    display_message = current_message
                    await asyncio.sleep(10)
            except Exception as e:
                LOGGER.info(str(e))
                pass
        if os.path.exists(download_file_path):
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await message.edit(f"Downloaded to <code>{download_file_path}</code> in <u>{ms}</u> seconds", parse_mode="html")
    else:
        await message.edit("`Reply to a Telegram Media, to download it to local server.`")


@Client.on_message(Filters.command("upload", COMMAND_HAND_LER) & Filters.me)
async def upload_as_document(client, message):
    status_message = await message.reply_text("`Uploading...`")
    if " " in message.text:
        local_file_name = message.text.split(" ", 1)[1]
        if os.path.exists(local_file_name):
            thumb_image_path = await is_thumb_image_exists(local_file_name)
            start_t = datetime.now()
            c_time = time.time()
            doc_caption = os.path.basename(local_file_name)
            await message.reply_document(
                document=local_file_name,
                thumb=thumb_image_path,
                caption=doc_caption,
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload", status_message, c_time
                )
            )
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await status_message.edit(f"**Uploaded in {ms} seconds**")
        else:
            await status_message.edit("404: media not found")
    else:
        await status_message.edit(f"<code>{COMMAND_HAND_LER}upload FILE_PATH</code> to upload to current Telegram chat")
    await message.delete()


@Client.on_message(Filters.command("batchup", COMMAND_HAND_LER) & Filters.me)
async def covid(client, message):
    if len(message.text.split(" ")) == 1:
        await message.edit("`Enter a directory location`")
    elif len(message.text.split(" ",1)) == 2:
        temp_dir = message.text.split(" ", 1)[1]
    else:
        await message.edit(f"__Please check help by using__ `{COMMAND_HAND_LER}help batchup`")
    status_message = await message.reply_text("`Uploading Files...`")
    if os.path.exists(temp_dir):
        files = os.listdir(temp_dir)
        files.sort()
        await status_message.edit("`Uploading Files to Telegram...`")
        for file in files:
            c_time = time.time()
            required_file_name = temp_dir+"/"+file
            thumb_image_path = await is_thumb_image_exists(required_file_name)
            doc_caption = os.path.basename(required_file_name)
            LOGGER.info(f"Uploading {required_file_name} from {temp_dir} to Telegram.")
            await client.send_document(
                chat_id=message.chat.id,
                document=required_file_name,
                thumb=thumb_image_path,
                caption=doc_caption,
                parse_mode="html",
                disable_notification=True,
                progress=progress_for_pyrogram,
                progress_args=(
                    "Trying to upload multiple files...", status_message, c_time)
                )
    else:
        await message.edit("Directory Not Found.")
        return
    await status_message.edit(f"Uploaded all files from Directory `{temp_dir}`")
