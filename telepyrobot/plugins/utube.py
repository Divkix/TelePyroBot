import os
import time
import asyncio
from datetime import datetime
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, MAX_MESSAGE_LENGTH
from telepyrobot.utils.run_shell_cmnd import run_command
from telepyrobot.utils.clear_string import clear_string

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Set yourself to afk.

If you're restart your bot, all counter and data in cache will be reset.
But you will still in afk, and always reply when got mentioned.

**Set AFK status**:
`{COMMAND_HAND_LER}afk <reason>` Set yourself to afk, give a reason if need.
* Reason is optional

whenever you send any message to any other chat that your `PRIVATE_GROUP_ID`,
the afk status would be set to False!
"""


@TelePyroBot.on_message(filters.command("ytv", COMMAND_HAND_LER) & filters.me)
async def tor_search(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1).lowercase()
    if ("youtube.com", "youtu.be") in link:
        ytdlv_cmd = [
            "youtube-dl",  # Main command
            "-f",  # Format
            "'(bestvideo[height>=720]+bestaudio/bestvideo+bestaudio)'",  # Best Video + best video
            "-vcio",  # Verbose, Continue download, Ignore errors, output format
            "'telepyrobot/downloads/%(title)s.%(ext)s'",  # Download Location
            "--write-description",  # Write Description file, if available
            "--write-auto-sub",  # Write auto subtitle file, if available
            "--merge-output-format mkv",  # Use mkv format
            link,  # Youtube link
        ]
        stdout, stderr = await run_command(ytdlv_cmd)

    OUTPUT += f"<b>stderr</b>: \n<code>{stderr}</code>\n\n"
    OUTPUT += f"<b>stdout</b>: \n<code>{stdout}</code>"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        OUTPUT = clear_string(OUTPUT)
        with BytesIO(str.encode(OUTPUT)) as f:
            f.name = "youtube-dl.txt"
            await m.reply_document(
                document=f,
                caption=link,
            )
        await m.delete()
    else:
        await m.edit_text(OUTPUT)
    return