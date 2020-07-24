import io
import os
import sys
import traceback
import time
import asyncio
import requests
from pyrogram import Client, Filters
from pyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
List the directories of the server.

`{COMMAND_HAND_LER}ls`: List files in ./ directory
`{COMMAND_HAND_LER}ls <diectory name>`: List all the files in the directory.
"""

@Client.on_message(Filters.command("ls", COMMAND_HAND_LER) & Filters.me)
async def list_directories(_, message):
    if len(message.command) == 1:
        cmd = "ls"
    elif len(message.command) >= 2:
        location = message.text.split(" ",1)[1]
        if (message.text.split(" ")[1]).lower in ("download", "downloads")
            location = "pyrobot/downloads"
        cmd = "ls " + location
    else:
        await message.edit("<b>Error:</b>\n<i>Check Help documentaion for Help</i>")

    reply_to_id = message.message_id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    OUTPUT = stdout.decode()
    if not OUTPUT:
        OUTPUT = "No Output"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await message.reply_document(
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("exec.text")
    else:
        await message.reply_text(OUTPUT)
