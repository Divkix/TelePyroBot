import requests
from time import sleep
import asyncio
import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ =  f"""
`{COMMAND_HAND_LER}cas <user_id>` or as a reply to the message to check the CAS status of the user.
"""

@Client.on_message(Filters.command("cas", COMMAND_HAND_LER) & Filters.me)
async def cas(client, message):
    cmd = message.text.split(' ', 1)
    user = ""
    if len(cmd) == 2:
        user = cmd[1]
    elif message.reply_to_message and len(cmd) == 1:
        user = message.reply_to_message.from_user.id
    else:
        await message.edit("**Usage:** `cas user_id`")
        await asyncio.sleep(2)
        await message.delete()
        return
    results = requests.get(f'https://api.cas.chat/check?user_id={user}').json()
    try:
        reply_text = f'`User ID: `{user}\n`Offenses: `{results["result"]["offenses"]}\n`Messages: `\n{results["result"]["messages"]}\n`Time Added: `{results["result"]["time_added"]}'
    except:
        reply_text = "`Record not found`"
    await message.edit(reply_text, parse_mode="md")
