import os
import time
import asyncio
import requests
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ =  f"""
Search for a query on google using userbot!

`{COMMAND_HAND_LER}gs <query>`
"""

@Client.on_message(Filters.command("gs", COMMAND_HAND_LER) & Filters.me)
async def google_s(client, message):
    input_str = message.text.split(" ",1)[1]
    sample_url = "https://da.gd/s?url=https://lmgtfy.com/?q={}%26iie=1".format(input_str.replace(" ","+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await message.edit("[{}]({})\n`Thank me Later 🙃` ".format(input_str, response_api.rstrip()))
    else:
        await message.edit("`Something is wrong. please try again later.``")
    return
