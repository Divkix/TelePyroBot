import os
import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}sdmsg <message> = <time in seconds>`

The command will automatically destruct the message after specified time.
"""

@Client.on_message(Filters.command("sdmsg", COMMAND_HAND_LER) & Filters.me)
async def self_destruct(client, message):
    input_str = message.text.split(" ", 1)[1]
    rm = await message.edit("`Meking self-destruct msg...`")
    ttl = 0
    if input_str:
        if "=" in input_str:
            message, ttl = input_str.split("=")
        else:
            await message.reply_text("__Check help to know how to use__")
            return
        if message.reply_to_message:
            reply_id = reply_to_message.message.id
            sd_msg = await reply_text(f"{message}", reply_to_message_id=reply_id)
        else:
            sd_msg = await reply_text(f"{message}")
        await rm.delete()
        await asyncio.sleep(int(ttl))
        await sd_msg.delete()
    else:
        await message.edit("__Check help to know how to use__")
        return
