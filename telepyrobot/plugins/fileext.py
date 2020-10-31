import os
import asyncio
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
import requests
from bs4 import BeautifulSoup

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}filext <file extension without '.'>`

This will fetch you information for file!
"""


@TelePyroBot.on_message(filters.command("filext", COMMAND_HAND_LER) & filters.me)
async def self_destruct(c: TelePyroBot, m: Message):
    if len(m.command) >= 2:
        await m.edit_text("Processing ...")
        sample_url = "https://www.fileext.com/file-extension/{}.html"
        input_str = m.text.split(" ", 1)[1]
        response_api = requests.get(sample_url.format(input_str))
        status_code = response_api.status_code
        if status_code == 200:
            raw_html = response_api.content
            soup = BeautifulSoup(raw_html, "html.parser")
            ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
            await m.edit_text(
                f"<b>File Extension:</b> `{input_str}`\n<b>Description:</b> `{ext_details}`"
            )
        else:
            await m.edit_text(
                f"https://www.fileext.com/ responded with {status_code} for query: {input_str}"
            )
    else:
        await m.edit_text("<i>Need a query to search for!</i>")
    return
