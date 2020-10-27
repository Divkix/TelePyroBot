import os
import time
import asyncio
import requests
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Search for a query on google using userbot!

`{COMMAND_HAND_LER}gs <query>`
"""


@TelePyroBot.on_message(filters.command("gs", COMMAND_HAND_LER) & filters.me)
async def google_s(c: TelePyroBot, m: Message):
    input_str = m.text.split(" ", 1)[1]
    sample_url = "https://da.gd/s?url=https://lmgtfy.com/?q={}%26iie=1".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await m.edit(
            "[{}]({})\n`Thank me Later 🙃` ".format(input_str, response_api.rstrip())
        )
    else:
        await m.edit("`Something is wrong. please try again later.``")
    return
