import io
import os
import sys
import traceback
import time
import asyncio
import requests
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER


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
        with open("exec.txt", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
            out_file.close()
        await m.reply_document(
            document="exec.txt",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove("exec.txt")
    else:
        await m.edit_text(OUTPUT)
    return
