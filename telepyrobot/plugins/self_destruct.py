import os
import asyncio
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.pyrohelpers import ReplyCheck

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}sdmsg <message> | <time in seconds>`

The command will automatically destruct the message after specified time.
"""


@TelePyroBot.on_message(filters.command("sdmsg", COMMAND_HAND_LER) & filters.me)
async def self_destruct(c: TelePyroBot, m: Message):
    input_str = m.text.split(None, 1)[1]
    rm = await m.edit_text("`Meking self-destruct msg...`")
    ttl = 0
    if input_str:
        if "=" in input_str:
            msg, ttl = input_str.split("|")
        else:
            await m.reply_text("__Check help to know how to use__")
            return
        sd_msg = await m.reply_text(f"{msg}", reply_to_message_id=ReplyCheck(m))
        await rm.delete()
        await asyncio.sleep(int(ttl))
        await sd_msg.delete()
    else:
        await m.edit_text("__Check help to know how to use__")
        return
