from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
import os
from telepyrobot import COMMAND_HAND_LER
import random
import time

p = 0

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Make quotes easily, from a message!
Does not work on images!
 
`{COMMAND_HAND_LER}qbot`: As a reply to message to get its quote
"""


@TelePyroBot.on_message(filters.command("qbot", COMMAND_HAND_LER) & filters.me)
async def quotly(c: TelePyroBot, m: Message):
    if not m.reply_to_message:
        await m.edit("Reply to any users text message")
        return
    await m.edit("`Making a Quote`")
    await m.reply_to_message.forward("@QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            msg = await c.get_history("@QuotLyBot", 1)
            check = msg[0]["sticker"]["file_id"]
            is_sticker = True
        except:
            time.sleep(0.5)
            progress += random.randint(0, 10)
            try:
                await m.edit(
                    "```Making a Quote```\nProcessing {}%".format(progress),
                    parse_mode="md",
                )
                if progress >= 100:
                    pass
            except Exception as ef:
                await m.edit(f"**ERROR:**\n{ef}", parse_mode="md")
                p += 1
                if p == 3:
                    break
    await m.edit("`Complete !`", parse_mode="md")
    msg_id = msg[0]["message_id"]
    await c.forward_messages(m.chat.id, "@QuotLyBot", msg_id)
    await c.read_history("@QuotLyBot")
    await m.delete()
