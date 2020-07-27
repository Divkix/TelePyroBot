import os
import time
import asyncio
from pyrogram import Client, Filters, ChatPermissions
from pyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN, PRIVATE_GROUP_ID, OWNER_ID, OWNER_NAME
from pyrobot.utils.admin_check import admin_check
from pyrobot.utils.parser import mention_markdown, escape_markdown
from pyrobot.utils.msg_types import Types, get_message_type
from pyrobot.utils.sql_helpers.afk_db import set_afk, get_afk


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__HELP__ = f"""
Set yourself to afk.

If you're restart your bot, all counter and data in cache will be reset.
But you will still in afk, and always reply when got mentioned.

**Set AFK status**:
`{COMMAND_HAND_LER}afk <reason>` Set yourself to afk, give a reason if need.
* reason is optional
"""

# Set priority to 11 and 12
MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 60  # seconds


@Client.on_message((Filters.command("afk", COMMAND_HAND_LER)) & Filters.me)
async def afk(client, message):
    if len(message.text.split()) >= 2:
        set_afk(True, message.text.split(None, 1)[1])
        await message.edit_text(
            "I am going AFK now...\nBecause of {}".format(message.text.split(None, 1)[1]))
        await client.send_message(PRIVATE_GROUP_ID,
            "You are AFK!\nBecause of {}".format(message.text.split(None, 1)[1]))
        await asyncio.sleep(3)
        await message.delete()
        
    else:
        set_afk(True, "")
        await message.edit_text(
            "{} is now AFK!".format(mention_markdown(message.from_user.id, message.from_user.first_name)))
        await client.send_message(PRIVATE_GROUP_ID,
            "{} is now AFK!".format(mention_markdown(message.from_user.id, message.from_user.first_name)))
        await asyncio.sleep(3)
        await message.delete()
    return


@Client.on_message(Filters.mentioned & ~Filters.bot, group=11)
async def afk_mentioned(client, message):
    global MENTIONED
    get = get_afk()
    if get and get['afk']:
        if "-" in str(message.chat.id):
            cid = str(message.chat.id)[4:]
        else:
            cid = str(message.chat.id)

        if cid in list(AFK_RESTIRECT) and int(AFK_RESTIRECT[cid]) >= int(
            time.time()
        ):
            return
        AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME
        if get['reason']:
            await message.reply_text(
                "Sorry, My Master {} is AFK right now!\nBecause of {}".format(mention_markdown(OWNER_ID, OWNER_NAME), get['reason']))
        else:
            await message.reply_text("Sorry, My Master {} is AFK right now!".format(mention_markdown(OWNER_ID, OWNER_NAME)))

        _, message_type = get_message_type(message)
        if message_type == Types.TEXT:
            text = message.text if message.text else message.caption
        else:
            text = message_type.name

        MENTIONED.append(
            {"user": message.from_user.first_name, "user_id": message.from_user.id, "chat": message.chat.title,
             "chat_id": cid, "text": text, "message_id": message.message_id})
        await client.send_message(PRIVATE_GROUP_ID, "{}({}) mentioned you in {}({})\nText:\n`{}`\n\nTotal count: `{}`".format(
            mention_markdown(message.from_user.id, message.from_user.first_name), message.from_user.id, message.chat.title, message.chat.id, text[:3500],
            len(MENTIONED)))
    await message.stop_propagation()


#@Client.on_message(Filters.me & Filters.group & ~Filters.group(PRIVATE_GROUP_ID), group=12)
@Client.on_message((Filters.command("unafk", COMMAND_HAND_LER)) & Filters.me)
async def no_longer_afk(client, message):
    global MENTIONED
    get = get_afk()
    unafkmsg = await message.edit("`No Longer AFK!`")
    if get and get['afk']:
        await client.send_message(PRIVATE_GROUP_ID, "No longer afk!")
        set_afk(False, "")
        text = "**Total {} mentioned you**\n".format(len(MENTIONED))
        for x in MENTIONED:
            msg_text = x["text"]
            if len(msg_text) >= 11:
                msg_text = "{}...".format(x["text"])
            text += "- [{}](https://t.me/c/{}/{}) ({}): {}\n".format(escape_markdown(x["user"]), x["chat_id"],
                                                                     x["message_id"], x["chat"], msg_text)
        await client.send_message(PRIVATE_GROUP_ID, text)
        await asyncio.sleep(3)
        await unafkmsg.detete()
        MENTIONED = []
        await message.stop_propagation()
