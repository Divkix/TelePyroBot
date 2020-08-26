import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}sdmsg <message> | <time in seconds>`

The command will automatically destruct the message after specified time.
"""


@Client.on_message(filters.command("sdmsg", COMMAND_HAND_LER) & filters.me)
async def self_destruct(c: Client, m: Message):
    input_str = message.text.split(" ", 1)[1]
    rm = await m.edit("`Meking self-destruct msg...`")
    ttl = 0
    if input_str:
        if "=" in input_str:
            msg, ttl = input_str.split("|")
        else:
            await m.reply_text("__Check help to know how to use__")
            return
        if m.reply_to_message:
            reply_id = reply_to_message.message.id
            sd_msg = await m.reply_text(f"{msg}", reply_to_message_id=reply_id)
        else:
            sd_msg = await m.reply_text(f"{msg}")
        await rm.delete()
        await asyncio.sleep(int(ttl))
        await sd_msg.delete()
    else:
        await m.edit("__Check help to know how to use__")
        return
