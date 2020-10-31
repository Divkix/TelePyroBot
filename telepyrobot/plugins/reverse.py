import os
from datetime import datetime
import shlex
import requests
from bs4 import BeautifulSoup
from typing import Tuple, Optional
from os.path import basename
import asyncio
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, LOGGER
from telepyrobot.utils.pyrohelpers import ReplyCheck

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))
__help__ = f"""
This module will help you Reverse Search Media

`{COMMAND_HAND_LER} reverse <reply to a media>`
Reverse search any supported media by: Google
"""
screen_shot = "telepyrobot/downloads/"


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """take a screenshot."""
    ttl = duration // 2
    thumb_image_path = path or os.path.join(screen_shot, f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await run_cmd(command))[1]
    if err:
        LOGGER.info(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


@TelePyroBot.on_message(filters.command("reverse", COMMAND_HAND_LER) & filters.me)
async def google_rs(c: TelePyroBot, m: Message):
    await m.edit_text("`Searching...`")
    start = datetime.now()
    out_str = "`Reply to an image`"
    if m.reply_to_message:
        message_ = m.reply_to_message
        if message_.sticker and message_.sticker.file_name.endswith(".tgs"):
            await m.edit_text("<b><i>Currently Not supported!</b></i>")
            return
        if message_.photo or message_.animation or message_.sticker:
            dis_loc = await c.download_media(message=message_)
        if message_.animation or message_.video:
            """await m.edit_text("`Converting this Gif`")
            img_file = os.path.join(screen_shot, "grs.jpg")
            await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await m.edit_text("`Something went wrong in Conversion`")
                await asyncio.sleep(5)
                await m.delete()"""
            await m.edit_text("<i>Currently not supported!</i>")
            return
            dis_loc = img_file
        base_url = "http://www.google.com"
        if dis_loc:
            search_url = f"{base_url}/searchbyimage/upload"
            multipart = {
                "encoded_image": (dis_loc, open(dis_loc, "rb")),
                "image_content": "",
            }
            google_rs_response = requests.post(
                search_url, files=multipart, allow_redirects=False
            )
            the_location = google_rs_response.headers.get("Location")
            os.remove(dis_loc)
        else:
            await m.delete()
            return
        await m.edit_text("`Found Google Results...`")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = base_url + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        end = datetime.now()
        ms = (end - start).seconds
        out_str = f"""<b>Time Taken</b>: {ms} seconds
<b>Possible Related Search</b>: <a href="{prs_url}">{prs_text}</a>
<b>More Info</b>: Open this <a href="{the_location}">Link</a>

Reverse search by: @TelePyroBot
"""
    await m.edit_text(out_str, parse_mode="HTML", disable_web_page_preview=True)
