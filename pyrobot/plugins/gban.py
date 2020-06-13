import time
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, GBAN_GROUP
import os

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}gban <username/userid> <gban reason>`: To gban a user.

`{COMMAND_HAND_LER}ungban <username/userid> <ungban reason>`: To ungban a user.
"""

@Client.on_message(Filters.command(["gban", "globalban"], COMMAND_HAND_LER) & Filters.me)
async def gban_user(client, message):
    await message.edit("`Initiating Global Ban for user...`")
    if len(message.command) >= 3:
        user_id = message.text.split(" ",2)[1]
        gban_reason = message.text.split(" ",2)[2]
        if user_id.startswith("@"):
            user_name = user_id
            await client.send_message(GBAN_GROUP, f"/gban {user_name} {gban_reason}")
        elif message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            await client.send_message(GBAN_GROUP, f"/gban [user](tg://user?id={user_id}) {gban_reason}")
        else:
            await client.send_message(GBAN_GROUP, f"/gban [user](tg://user?id={user_id}) {gban_reason}")
    else:
        await message.edit("`Please give a proper **user_id** or **gban_reason**`")
        return
    await client.read_history(GBAN_GROUP)
    await message.edit("`User has been gbanned!`")


@Client.on_message(Filters.command(["ungban", "unglobalban", "gunban", "globalunban"], COMMAND_HAND_LER) & Filters.me)
async def ungban_user(client, message):
    await message.edit("`Initiating Global UnBan for user...`")
    if len(message.command) >= 3:
        user_id = message.text.split(" ",2)[1]
        ungban_reason = message.text.split(" ",2)[2]
        if user_id.startswith("@"):
            user_name = user_id
            await client.send_message(GBAN_GROUP, f"/ungban {user_name} {ungban_reason}")
        elif message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            await client.send_message(GBAN_GROUP, f"/ungban [user](tg://user?id={user_id}) {ungban_reason}")
        else:
            await client.send_message(GBAN_GROUP, f"/ungban [user](tg://user?id={user_id}) {ungban_reason}")
    else:
        await message.edit("`Please give a proper **user_id** or **ungban_reason**`")
        return
    await client.read_history(GBAN_GROUP)
    await message.edit("`User has been ungbanned!`")
