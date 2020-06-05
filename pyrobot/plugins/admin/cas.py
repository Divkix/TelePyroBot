import requests
from time import sleep
import asyncio

from pyrobot.helper_functions.misc.PyroHelpers import ReplyCheck
from pyrobot.helper_functions.misc.string import replace_text

from pyrogram import Client, Filters, Message, User
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter

from pyrogram.api import functions
from pyrogram.errors import PeerIdInvalid

@Client.on_message(Filters.command("cas", COMMAND_HAND_LER) & sudo_filter)
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
    await message.edit(replace_text(reply_text))
