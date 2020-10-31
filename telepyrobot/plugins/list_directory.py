import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER
from telepyrobot.utils.clear_string import clear_string
from telepyrobot.utils.check_size import get_size_format

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
List the directories of the server.

`{COMMAND_HAND_LER}ls`: List files in ./ directory
`{COMMAND_HAND_LER}ls <diectory name>`: List all the files in the directory.
"""

def get_directory_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return get_size_format(total)


@TelePyroBot.on_message(filters.command("ls", COMMAND_HAND_LER) & filters.me)
async def list_directories(c: TelePyroBot, m: Message):
    if len(m.command) == 1:
        location = "."
        OUTPUT = f"Files in <code>/root/</code>:\n\n"
    elif len(m.command) >= 2:
        location = m.text.split(" ", 1)[1]
        OUTPUT = f"Files in <code>{location}</code>:\n\n"

    files = os.listdir(location)
    reply_to_id = m.message_id
    files.sort()  # Sort the files

    for file in files:
        OUTPUT += f"<code>{file}</code> ({get_directory_size(file)})\n"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        # OUTPUT = clear_string(OUTPUT)  # Remove the html elements using regex
        with open("ls.txt", "w+", encoding="utf8") as out_file:
            out_file.write(OUTPUT)
        await m.reply_document(
            document="ls.txt",
            caption=f"{location} ({get_directory_size(location)})")
        await m.delete()
        os.remove("ls.txt")
    else:
        await m.edit_text(OUTPUT)
    return
