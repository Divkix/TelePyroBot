import time
import os
import random
from pyrogram.errors import FloodWait
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, LOGGER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Get text typed in typewriter format.

`{COMMAND_HAND_LER}type <text>` / `{COMMAND_HAND_LER}typewriter <text>`
"""


@TelePyroBot.on_message(
    filters.command(["type", "typewriter"], COMMAND_HAND_LER) & filters.me
)
async def upload_as_document(c: TelePyroBot, m: Message):
    text = m.command[1:]
    if not text:
        await m.edit_text("`Input not found`")
        return
    s_time = 0.1
    typing_symbol = "|"
    old_text = ""
    await m.edit_text(typing_symbol)
    time.sleep(s_time)
    for character in text:
        s_t = s_time / random.randint(1, 100)
        old_text += character
        typing_text = old_text + typing_symbol
        try:
            await m.try_to_edit(typing_text, sudo=False)
            time.sleep(s_t)
            await m.try_to_edit(old_text, sudo=False)
            time.sleep(s_t)
        except FloodWait as ef:
            time.sleep(ef.x)
            LOGGER.info(str(ef))
        return
