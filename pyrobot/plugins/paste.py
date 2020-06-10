import aiohttp
import json
import os
from urllib.parse import urlparse
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY
import os

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}paste`: as a reply to text message to paste it to nekobin.

`{COMMAND_HAND_LER}paste <nekobin>`/<deldog>/<dogbin>: to use a specific service for paste.
"""

@Client.on_message(Filters.command("paste", COMMAND_HAND_LER))
async def paste_bin(client, message):
    await message.edit("`Pasting...`")
    downloaded_file_name = None

    if message.reply_to_message and message.reply_to_message.media:
        downloaded_file_name_res = await message.reply_to_message.download(
            file_name=TMP_DOWNLOAD_DIRECTORY
        )
        m_list = None
        with open(downloaded_file_name_res, "rb") as fd:
            m_list = fd.readlines()
        downloaded_file_name = ""
        for m in m_list:
            downloaded_file_name += m.decode("UTF-8")
            downloaded_file_name += "\n"
        os.remove(downloaded_file_name_res)
    elif message.reply_to_message:
        downloaded_file_name = message.reply_to_message.text.html
    else:
        await message.edit("What do you want to Paste?")
        return

    if downloaded_file_name is None:
        await message.edit("What do you want to Paste?")
        return

    json_paste_data = {
        "content": downloaded_file_name
        }

    # a dictionary to store different pastebin URIs
    paste_bin_store_s = {
        "deldog": "https://del.dog/documents",
        "nekobin": "https://nekobin.com/api/documents",
        "dogbin": "https://del.dog/documents"
        }

    default_paste = "nekobin"
    if len(message.command) == 2:
        default_paste = message.text.split(' ', 1)[1]

    paste_store_url = paste_bin_store_s.get(default_paste, paste_bin_store_s["nekobin"])
    paste_store_base_url_rp = urlparse(paste_store_url)

    paste_store_base_url = paste_store_base_url_rp.scheme + "://" + \
        paste_store_base_url_rp.netloc

    async with aiohttp.ClientSession() as session:
        response_d = await session.post(paste_store_url, json=json_paste_data)
        response_jn = await response_d.json()

    t_w_attempt = bleck_megick(response_jn)
    required_url = json.dumps(t_w_attempt, sort_keys=True, indent=4) + "\n\n #ERROR"
    if t_w_attempt is not None:
        required_url = paste_store_base_url + "/" + "raw" + "/" + t_w_attempt
    await message.edit(f"**Pasted to {default_paste}**:\n{required_url}")


def bleck_megick(dict_rspns):
    first_key_r = dict_rspns.get("key")
    if first_key_r is not None:
        return first_key_r
    check_if_result_ests = dict_rspns.get("result")
    if check_if_result_ests is not None:
        second_key_a = check_if_result_ests.get("key")
        if second_key_a is not None:
            return second_key_a
    return None
