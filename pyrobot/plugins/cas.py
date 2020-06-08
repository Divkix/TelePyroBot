import requests
from time import sleep
import asyncio

from pyrobot.utils.misc.PyroHelpers import ReplyCheck
from pyrobot.utils.misc.string import replace_text

from pyrogram import Client, Filters, Message, User
from pyrobot import COMMAND_HAND_LER


from pyrogram.api import functions
from pyrogram.errors import PeerIdInvalid

@Client.on_message(Filters.command("cas", COMMAND_HAND_LER) & Filters.me)
async def cas(client, message):
    cmd = message.command
    user = ""
    if len(cmd) > 1:
        user = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        user = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Usage: cas user_id`")
        await asyncio.sleep(2)
        await message.delete()
        return
    results = requests.get(f'https://api.cas.chat/check?user_id={user}').json()
    try:
        reply_text = f'`User ID: `{user}\n`Offenses: `{results["result"]["offenses"]}\n`Messages: `\n{results["result"]["messages"]}\n`Time Added: `{results["result"]["time_added"]}'
    except:
        reply_text = "`Record not found.`"
    await message.edit(replace_text(reply_text), parse_mode="md")
