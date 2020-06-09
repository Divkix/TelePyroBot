import time
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, GBAN_GROUP

__PLUGIN__ = "Global Ban"

__help__ = f"""
{COMMAND_HAND_LER}gban <username/userid> <gban reason>: To gban a user.

{COMMAND_HAND_LER}ungban <username/userid> <gban reason>: To ungban a user.
"""

@Client.on_message(Filters.command(["gban", "globalban"], COMMAND_HAND_LER) & Filters.me)
async def gban_user(client, message):
    await message.edit("`Initiating Global Ban for user...`")
    if len(message.command) == 2:
        user_id = message.text.split(" ",2)[1]
    elif message.reply_to_message and len(message.command) == 1:
        user_id = message.reply_to_message.from_user.id
    gban_reason = message.text.split(" ",2)[2]
    await client.send_message(GBAN_GROUP, f"/gban [user](tg://user?id={user_id}) {gban_reason}")
    time.sleep(1)
    msg = await client.get_history(GBAN_GROUP, 1)
    msg_id = msg[0]["message_id"]
    await client.read_history(GBAN_GROUP)
    await message.edit("`User has been gbanned!`")

@Client.on_message(Filters.command(["ungban", "unglobalban", "gunban", "globalunban"], COMMAND_HAND_LER) & Filters.me)
async def ungban_user(client, message):
    await message.edit("`Initiating Global Unban for user...`")
    if len(message.command) == 2:
        user_id = message.text.split(" ",2)[1]
    elif message.reply_to_message and len(message.command) == 1:
        user_id = message.reply_to_message.from_user.id
    gban_reason = message.text.split(" ",2)[2]
    await client.send_message(GBAN_GROUP, f"/ungban [user](tg://user?id={user_id}) {gban_reason}")
    time.sleep(1)
    msg = await client.get_history(GBAN_GROUP, 1)
    msg_id = msg[0]["message_id"]
    await client.read_history(GBAN_GROUP)
    await message.edit("`User has been ungbanned!`")
