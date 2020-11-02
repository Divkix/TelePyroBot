from io import BytesIO
import os
import sys
import traceback
import time
import asyncio
import requests
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER
from telepyrobot.utils.clear_string import clear_string


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Get System information!!
`{COMMAND_HAND_LER}neofetch`

Will fetch basic information about your bot's machine.
"""


@TelePyroBot.on_message(filters.command("neofetch", COMMAND_HAND_LER) & filters.me)
async def neofetch_stats(c: TelePyroBot, m: Message):
    cmd = "neofetch --stdout"

    reply_to_id = m.message_id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    OUTPUT = stdout.decode()
    if not OUTPUT:
        OUTPUT = "No Output"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        OUTPUT = clear_string(OUTPUT)  # Remove the html elements using regex
        with BytesIO(str.encode(OUTPUT)) as f:
            f.name = "neofetch.txt"
            await m.reply_document(document=f, caption=f"<code>{cmd}</code>")
        await m.delete()
    else:
        await m.edit_text(OUTPUT)
    return
