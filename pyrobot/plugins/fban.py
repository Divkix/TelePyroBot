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
    if len(message.command) >= 3:
        cmd = message.text.split(" ",1)
        fban_string = cmd[1]
    elif len(message.command) == 2:
        cmd = message.text.split(" ",1)
        fban_string = cmd[1]
    elif message.reply_to_message:
        fban_user = message.reply_to_message.from_user.id
        from_user = await client.get_users(fban_user)
        if cmd[1]:
            fban_string = from_user.id + " " + cmd[1]
        else:
            fban_string = from_user.id
    else:
        await message.edit("`Use Proper format to fban a user, check help for more information`")
        return
    await client.send_message("@MissRose_bot", f"/fban {fban_string}")
    time.sleep(1)
    msg = await client.get_history("@MissRose_bot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@MissRose_bot", msg_id)
    await client.read_history("@MissRose_bot")
    await message.delete()


@Client.on_message(Filters.command("unfban", COMMAND_HAND_LER) & Filters.me)
async def unfban_user(client, message):
    if len(message.command) == 2:
        unfban_user = message.text.split(" ",1)[1]
    elif message.reply_to_message:
        unfban_user = message.reply_to_message.from_user.id
        from_user = await client.get_users(unfban_user)
    else:
        await message.edit("`Use Proper format to unfban a user, check help for more information`")
        return
    await client.send_message("@MissRose_bot", f"/unfban {from_user.id}")
    time.sleep(1)
    msg = await client.get_history("@MissRose_bot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@MissRose_bot", msg_id)
    await client.read_history("@MissRose_bot")
    await message.delete()


@Client.on_message(Filters.command(["fstat", "fbanstat"], COMMAND_HAND_LER) & Filters.me)
async def fstat_user(client, message):
    if len(message.command) <= 3:
        if len(message.command) == 2:
            fstat_user = message.text.split(" ",1)[1]
            await client.send_message("@MissRose_bot", f"/fstat {fstat_user}")
        elif len(message.command) == 3:
            fstat_user = message.text.split(" ",1)[1]
            fstat_id = message.text.split(" ",1)[2]
            await client.send_message("@MissRose_bot", f"/fstat {fstat_user} {fstat_id}")
        else:
            await message.edit(f"Please check {COMMAND_HAND_LER}help on how to use")
    elif message.reply_to_message:
        if len(message.command) == 1:
            fstat_user = message.reply_to_message.from_user.id
            await client.send_message("@MissRose_bot", f"/fstat {fstat_user}")
        elif len(message.command) == 2:
            fstat_user = message.reply_to_message.from_user.id
            fstat_id = message.text.split(" ",1)[2]
            await client.send_message("@MissRose_bot", f"/fstat {fstat_user} {fstat_id}")
        else:
            await message.edit(f"Please check {COMMAND_HAND_LER}help on how to use")
    else:
        await client.send_message("@MissRose_bot", "/fstat")
    time.sleep(1)
    msg = await client.get_history("@MissRose_bot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@MissRose_bot", msg_id)
    await client.read_history("@MissRose_bot")
    await message.delete()
