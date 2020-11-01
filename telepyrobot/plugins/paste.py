import aiohttp
import json
import os
from io import BytesIO
from urllib.parse import urlparse
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY
from telepyrobot.utils.clear_string import clear_string
import os

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}paste`: as a reply to text message to paste it to nekobin.

`{COMMAND_HAND_LER}paste <nekobin>`/<deldog>/<dogbin>: to use a specific service for paste.
"""


@TelePyroBot.on_message(filters.command("paste", COMMAND_HAND_LER))
async def paste_bin(c: TelePyroBot, m: Message):
    await m.edit_text("`Pasting...`")
    downloaded_file_name = None

    if m.reply_to_message and m.reply_to_message.media:
        filename_loc = await m.reply_to_message.download(
            file_name=TMP_DOWNLOAD_DIRECTORY
        )
        m_list = None
        with open(filename_loc, "rb") as fd:
            m_list = fd.readlines()
            fd.close()
        downloaded_file_name = ""
        for m in m_list:
            downloaded_file_name += m.decode("UTF-8")
            downloaded_file_name += "\n"
        os.remove(filename_loc)
    elif m.reply_to_message:
        downloaded_file_name = m.reply_to_message.text.html
    else:
        await m.edit_text("What do you want to Paste?")
        return

    if downloaded_file_name is None:
        await m.edit_text("What do you want to Paste?")
        return

    json_paste_data = {"content": downloaded_file_name}

    # a dictionary to store different pastebin URIs
    paste_bin_store_s = {
        "deldog": "https://del.dog/documents",
        "nekobin": "https://nekobin.com/api/documents",
        "dogbin": "https://del.dog/documents",
    }

    default_paste = "nekobin"
    if len(m.text.split()) == 2:
        default_paste = m.text.split(" ", 1)[1]

    paste_store_url = paste_bin_store_s.get(default_paste, paste_bin_store_s["nekobin"])
    paste_store_base_url_rp = urlparse(paste_store_url)

    paste_store_base_url = (
        paste_store_base_url_rp.scheme + "://" + paste_store_base_url_rp.netloc
    )

    async with aiohttp.ClientSession() as session:
        response_d = await session.post(paste_store_url, json=json_paste_data)
        response_jn = await response_d.json()

    t_w_attempt = key_nikalo(response_jn)
    required_url = json.dumps(t_w_attempt, sort_keys=True, indent=4) + "\n\n #ERROR"
    if t_w_attempt is not None:
        required_url = paste_store_base_url + "/" + t_w_attempt
    await m.edit_text(
        f"**Pasted to {default_paste}**:\n{required_url}", disable_web_page_preview=True
    )


def key_nikalo(dict_rspns):
    first_key_r = dict_rspns.get("key")
    if first_key_r is not None:
        return first_key_r
    check_if_result_ests = dict_rspns.get("result")
    if check_if_result_ests is not None:
        second_key_a = check_if_result_ests.get("key")
        if second_key_a is not None:
            return second_key_a
    return None
