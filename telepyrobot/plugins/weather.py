from html import escape
import requests
import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Get current weather in your location
`{COMMAND_HAND_LER}weather <location>`

Powered by: https://wttr.in
"""


@TelePyroBot.on_message(filters.command("weather", COMMAND_HAND_LER) & filters.me)
async def weather(c: Client, m: Message):
    if len(message.text.split()) == 1:
        await m.edit(
            f"Usage: `{COMMAND_HAND_LER}weather <location>`", parse_mode="markdown"
        )
        return
    location = message.text.split(None, 1)[1]
    h = {"user-agent": "httpie"}
    a = requests.get(f"https://wttr.in/{location}?mnTC0&lang=en", headers=h)
    if (
        "Sorry, we processed more than 1M requests today and we ran out of our datasource capacity."
        in a.text
    ):
        await m.edit("Sorry!\nCannot fetch info, api full!")
        return
    weather = f"<code>{escape(a.text)}</code>"
    await m.edit(weather, parse_mode="html")
