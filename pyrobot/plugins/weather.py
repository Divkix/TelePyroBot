from html import escape
import requests
import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = """
Get current weather in your location
──「 **Weather** 」──
-> `weather (location)`
Get current weather in your location.
Powered by `wttr.in`
"""

@Client.on_message(Filters.command("weather", COMMAND_HAND_LER) & Filters.me)
async def weather(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `weather Maldives`")
        return
    location = message.text.split(None, 1)[1]
    h = {'user-agent': 'httpie'}
    a = requests.get(f"https://wttr.in/{location}?mnTC0&lang=en", headers=h)
    if "Sorry, we processed more than 1M requests today and we ran out of our datasource capacity." in a.text:
        await message.edit("Sorry, location not found!")
        return
    weather = f"<code>{escape(a.text)}</code>"
    await message.edit(weather, parse_mode='html')
