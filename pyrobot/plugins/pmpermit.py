import re
import os
import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, LOGGER, OWNER_ID, PM_PERMIT, PRIVATE_GROUP_ID, OWNER_NAME
from pyrobot.utils.parser import mention_markdown
from pyrobot.utils.sql_helpers.pmpermit_db import set_whitelist, get_whitelist, del_whitelist

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Create groups easily with userbot!
Annoyed from People sending you private messages? :v
Here is the solution, whenever people
"""

BLACKLIST = ["hack", "fuck", "bitch", "pubg", "sex"]

welc_txt = f"""
Hello, I'm {OWNER_NAME}'s Userbot.
Please leave your message and my Owner will contact you shortly!
"""

@Client.on_message(~Filters.me & Filters.private & ~Filters.bot)
async def pm_block(client, message):
    if not PM_PERMIT:
        return
    if not get_whitelist(message.chat.id):
        if message.text:
            for x in message.text.lower().split():
                if x in BLACKLIST:
                    await message.reply(
                        "You triggered a blaclist word\nI'm blocking you mf + reporting, don't contact me again!")
                    await client.block_user(message.chat.id)
                    return
                else:
                    await message.reply_text(welc_txt)
                    await asyncio.sleep(2)
                    await client.send_message(PRIVATE_GROUP_ID, "{} **wants to contact you in PM**".format(mention_markdown(message.from_user.id, message.from_user.first_name)))    


@Client.on_message(Filters.me & Filters.command(["approve", "pm"], COMMAND_HAND_LER) & Filters.private)
async def approve_pm(client, message):
    set_whitelist(message.chat.id, True)
    await message.edit("**__PM permission was approved!__**")
    await asyncio.sleep(5)
    await message.delete()


@Client.on_message(Filters.me & Filters.command(["revoke", "disapprove", "dispm"], COMMAND_HAND_LER) & Filters.private)
async def revoke_pm_block(client, message):
    del_whitelist(message.chat.id)
    await message.edit("__**PM permission was revoked!**__")
    await asyncio.sleep(5)
    await message.delete()
