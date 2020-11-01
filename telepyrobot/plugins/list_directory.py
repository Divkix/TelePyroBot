import os
from io import BytesIO
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER
from telepyrobot.utils.clear_string import clear_string
from telepyrobot.utils.check_size import get_directory_size

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
List the directories of the server.

`{COMMAND_HAND_LER}ls`: List files in ./ directory
`{COMMAND_HAND_LER}ls <directory name>`: List all the files in the directory.
"""


@TelePyroBot.on_message(filters.command("ls", COMMAND_HAND_LER) & filters.me)
async def list_directories(c: TelePyroBot, m: Message):
    if len(m.text.split()) == 1:
        location = "."
    elif len(m.text.split()) >= 2:
        location = m.text.split(None, 1)[1]

    location = os.path.abspath(location)
    if not location.endswith("/"):
        location += "/"
    OUTPUT = f"Files in <code>{location}</code>:\n\n"

    files = os.listdir(location)
    files.sort()  # Sort the files

    for file in files:
        OUTPUT += f"<code>{file}</code> ({get_directory_size(os.path.abspath(location+file))})\n"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        OUTPUT = clear_string(OUTPUT)  # Remove the html elements using regex
        with BytesIO(str.encode(OUTPUT)) as f:
            f.name = "ls.txt"
            await m.reply_document(
                document=f,
                caption=f"{location} ({get_directory_size(os.path.abspath(location))})",
            )
        await m.delete()
    else:
        if OUTPUT.endswith("\n\n"):
            await m.edit_text(f"No files in {location}")
            return
        await m.edit_text(OUTPUT)

    return
