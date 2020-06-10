import time
import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}fban <username/userid> <reason>`: To fban a user.

`{COMMAND_HAND_LER}unfban <username/userid>`: To unfban a user.

`{COMMAND_HAND_LER}fstat <username/userid>`: To get fstat of a user.
"""

@Client.on_message(Filters.command("fban", COMMAND_HAND_LER) & Filters.me)
async def fban_user(client, message):
    if len(message.command) == 3:
        fban_user = message.text.split(" ",2)[1]
        fban_reason = message.text.split(" ",2)[2]
    elif message.reply_to_message and len(message.command) == 2:
        fban_user = message.reply_to_message.from_user.id
        fban_reason = message.text.split(" ",1)[1]
    await client.send_message("@MissRose_bot", f"/fban {fban_user} {fban_reason}")
    time.sleep(1)
    msg = await client.get_history("@MissRose_bot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@MissRose_bot", msg_id)
    await client.read_history("@MissRose_bot")
    await message.delete()


@Client.on_message(Filters.command("unfban", COMMAND_HAND_LER) & Filters.me)
async def unfban_user(client, message):
    if len(message.command) == 2:
        unfban_user = message.text.split(" ",2)[1]
    elif message.reply_to_message and len(message.command) == 1:
        unfban_user = message.reply_to_message.from_user.id
    await client.send_message("@MissRose_bot", f"/unfban {unfban_user}")
    time.sleep(1)
    msg = await client.get_history("@MissRose_bot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@MissRose_bot", msg_id)
    await client.read_history("@MissRose_bot")
    await message.delete()


@Client.on_message(Filters.command("fstat", COMMAND_HAND_LER) & Filters.me)
async def fstat_user(client, message):
    if len(message.command)==2:
        fstat_user = message.text.split(" ",1)[1]
        await client.send_message("@MissRose_bot", f"/fstat {fstat_user}")
    elif message.reply_to_message and len(message.command) == 1:
        fstat_user = message.reply_to_message.from_user.id
        await client.send_message("@MissRose_bot", f"/fstat {fstat_user}")
    else:
        await client.send_message("@MissRose_bot", "/fstat")
    time.sleep(1)
    msg = await client.get_history("@MissRose_bot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@MissRose_bot", msg_id)
    await client.read_history("@MissRose_bot")
    await message.delete()
