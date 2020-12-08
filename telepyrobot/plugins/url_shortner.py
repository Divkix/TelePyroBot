import requests
import os
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Url Shortner Plugin for https://da.gd

**Usage:**
`{COMMAND_HAND_LER}short <long-link>`: Will return shortlink of the long-link.
`{COMMAND_HAND_LER}unshort <shortlink>`: Will return long url of the shortlink.
"""


@TelePyroBot.on_message(filters.command("short", COMMAND_HAND_LER) & filters.me)
async def short_link(c: TelePyroBot, m: Message):
    input_str = m.text.split(None, 1)[1]
    sample_url = f"https://da.gd/s?url={input_str}"
    response_api = requests.get(sample_url).text
    if response_api:
        await m.edit_text(f"**Generated Link:**\n {response_api} for {input_str}.")
    else:
        await m.edit_text("something is wrong. please try again later.")


@TelePyroBot.on_message(filters.command("unshort", COMMAND_HAND_LER) & filters.me)
async def unshort_link(c: TelePyroBot, m: Message):
    input_str = m.text.split(None, 1)[1]
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    if not input_str.startswith("http://da.gd"):
        await m.edit_text("`I can only unshort da.gd links`")
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await m.edit_text(
            f"Input URL: {input_str}\nReDirected URL: {r.headers['Location']}"
        )
    else:
        await m.edit_text(f"Input URL {input_str} returned status_code {r.status_code}")
