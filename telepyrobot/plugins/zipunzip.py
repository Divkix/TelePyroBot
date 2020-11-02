import asyncio
import os
import zipfile
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Easily Check CAS ban of a user!
`{COMMAND_HAND_LER}zip <folder>` to the zip the folder.
"""


async def zipdir(path):
    if path.endswith("/"):
        path = path[0:-1]
    filename = path.split("/")[-1] + ".zip"
    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file))
    return filename


async def unzipfiles(zippath):
    foldername = zippath.split("/")[-1]
    extract_path = f"/root/telepyrobot/cache/unzip/{foldername}"
    with zipfile.ZipFile(zippath, "r") as f:
        f.extractall(extract_path)
    return extract_path


@TelePyroBot.on_message(filters.command("zip", COMMAND_HAND_LER) & filters.me)
async def zipit(c: TelePyroBot, m: Message):
    if (m.command) == 1:
        await m.edit_text("Please enter a directory path to zip!")
        return
    location = m.text.split(None, 1)[1]
    await m.edit_text("<code>Zipping file...</code>")
    filename = await zipdir(location)
    await m.edit_text(
        f"File zipped and saved to <code>/root/{filename}</code>, to upload, use <code>{COMMAND_HAND_LER}upload {filename}</code>"
    )
    return


@TelePyroBot.on_message(filters.command("unzip", COMMAND_HAND_LER) & filters.me)
async def unzipit(c: TelePyroBot, m: Message):
    if (m.command) == 1:
        await m.edit_text("Please enter path to zip file which you want to extract!")
        return
    fileLoc = m.text.split(None, 1)[1]
    if not fileLoc.endswith(".zip"):
        await m.edit_text("Can only unzip <code>.zip</code> files!")
        return

    await m.edit_text("<code>Unzipping file...</code>")
    extract_path = await unzipfiles(fileLoc)
    await m.edit_text(f"Files unzipped to <code>{extract_path}</code>.")
    return