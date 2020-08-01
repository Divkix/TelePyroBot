import re
import os
import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, LOGGER, OWNER_ID, PM_PERMIT, PRIVATE_GROUP_ID, OWNER_NAME
from pyrobot.utils.parser import mention_markdown
from pyrobot.utils.sql_helpers import pmpermit_db as db
from pyrobot.utils.cust_p_filters import sudo_filter
from pyrobot.utils.pyrohelpers import extract_user

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Annoyed from People sending you private messages? :v
Here is the solution, whenever people text you, It'll show them
a message that you are not available
"""

BLACKLIST = ["hack", "fuck", "bitch", "pubg", "sex"]

welc_txt = f"""
Hello, I'm {OWNER_NAME}'s Userbot.
Please leave your message and my Owner will contact you shortly!

If you spam, You'll be blocked + reported
"""

@Client.on_message(Filters.private & (~Filters.me & ~Filters.bot & ~sudo_filter), group=3)
async def pm_block(client, message):
    if not PM_PERMIT:
        return
    if not db.get_whitelist(message.chat.id):
        if db.get_msg_id(message.chat.id):
            old_msg_id = db.get_msg_id(message.chat.id)
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=old_msg_id)
        if message.text:
            for x in message.text.lower().split():
                if x in BLACKLIST:
                    await message.reply(
                        "You triggered a blacklist word\nI'm blocking you mf + reporting, don't contact my master again!")
                    await client.block_user(message.chat.id)
                    await client.send_message(PRIVATE_GROUP_ID, "{} **was blocked due to a blacklist word!**".format(mention_markdown(message.from_user.id, message.from_user.first_name)))
                    return
        
        await message.reply_text(welc_txt)
        db.set_last_msg_id(message.chat.id, message.message_id)
        await asyncio.sleep(2)
        await client.send_message(PRIVATE_GROUP_ID, "{} **wants to contact you in PM**".format(mention_markdown(message.from_user.id, message.from_user.first_name)))
        return


@Client.on_message(Filters.me & Filters.command(["approve", "pm"], COMMAND_HAND_LER) & Filters.private)
async def approve_pm(client, message):
    if message.chat.type == "private":
        user_id = message.chat.id
    else:
        user_id, user_first_name = extract_user(message)
    db.set_whitelist(user_id, True)
    old_msg_id = db.get_msg_id(message.chat.id)
    if old_msg_id:
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=old_msg_id)
    user = await client.get_users(user_id)
    await message.edit("**__PM permission was approved__** for {}".format(mention_markdown(user_id, user.first_name)))
    await client.send_message(PRIVATE_GROUP_ID, "{} **is approved to contact you in PM!**".format(mention_markdown(user_id, user.first_name)))
    await asyncio.sleep(5)
    await message.delete()


@Client.on_message(Filters.me & Filters.command(["revoke", "disapprove", "dispm"], COMMAND_HAND_LER) & Filters.private)
async def revoke_pm_block(client, message):
    if message.chat.type == "private":
        user_id = message.chat.id
    else:
        user_id = message.text.split(" ")[1]
    db.del_whitelist(user_id)
    user = await client.get_users(user_id)
    await message.edit("__**PM permission was revoked for**__ {}".format(mention_markdown(user_id, user.first_name)))
    user_id = message.chat.id
    await client.send_message(PRIVATE_GROUP_ID, "{}'s **permission to contact you in PM has been revoked!**".format(mention_markdown(user_id, user.first_name)))
    await asyncio.sleep(5)
    await message.delete()