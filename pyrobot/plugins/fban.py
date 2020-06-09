import time
from pyrogram import Client, Filters
from pyrobot.utils.list_to_string import listToString
from pyrobot import COMMAND_HAND_LER

@Client.on_message(Filters.command("fban", COMMAND_HAND_LER) & Filters.me)
async def fban_user(client, message):
    fban_user = listToString(message.command[1])
    fban_reason = listToString(message.command[2:])
    await client.send_message("@MissRose_bot", f"/fban {fban_user} {fban_reason}")
    time.sleep(1)
    msg = await client.get_history("@MissRose_bot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@MissRose_bot", msg_id)
    await client.read_history("@MissRose_bot")
    await message.delete()


@Client.on_message(Filters.command("unfban", COMMAND_HAND_LER) & Filters.me)
async def unfban_user(client, message):
    unfban_user = listToString(message.command[1])
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
        fstat_user = listToString(message.command[1])
        await client.send_message("@MissRose_bot", f"/fstat {fstat_user}")
    elif message.reply_to_message:
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
