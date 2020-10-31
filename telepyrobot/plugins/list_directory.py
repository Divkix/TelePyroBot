import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
List the directories of the server.

`{COMMAND_HAND_LER}ls`: List files in ./ directory
`{COMMAND_HAND_LER}ls <diectory name>`: List all the files in the directory.
"""


@TelePyroBot.on_message(filters.command("ls", COMMAND_HAND_LER) & filters.me)
async def list_directories(c: TelePyroBot, m: Message):
    if len(m.command) == 1:
        location = "."
    elif len(m.command) >= 2:
        location = m.text.split(" ", 1)[1]

    files = os.listdir(location)
    reply_to_id = m.message_id
    files.sort()  # Sort the files

    OUTPUT = f"Files in __{location}__:\n\n"

    for file in files:
        OUTPUT += f"<code>{file}</code>\n"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with open("ls.txt", "w+", encoding="utf8") as out_file:
            out_file.write(OUTPUT)
        await m.reply_document(
            document="ls.txt",
            caption=location)
        await m.delete()
        os.remove("ls.txt")
    else:
        await m.edit_text(OUTPUT)
    return
