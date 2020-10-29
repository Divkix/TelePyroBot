from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.pyrohelpers import ReplyCheck
from requests import post
import shutil
import os
from time import sleep

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}carbon` <text> or as a reply to the message.
"""

CARBON_LANG = "Auto"


@TelePyroBot.on_message(filters.command("carbon", COMMAND_HAND_LER) & filters.me)
async def carbon_api(c: TelePyroBot, m: Message):
    json = {
        "backgroundColor": "rgba(0, 255, 230, 100)",
        "theme": "Dracula",
        "exportSize": "4x",
    }
    cmd = m.command
    if m.reply_to_message:
        r = m.reply_to_message
        json["code"] = r.text
        await m.edit_text("`Carbonizing code...`")
    elif len(cmd) >= 2:
        r = m.text.split(" ", 1)[1]
        json["code"] = r
    else:
        await m.edit(f"Usage: `{COMMAND_HAND_LER}carbon` <reply to a code or text>")
    json["language"] = CARBON_LANG
    apiUrl = "http://carbonnowsh.herokuapp.com"
    r = post(apiUrl, json=json, stream=True)
    filename = "carbon.png"
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)
            f.close()
        await c.send_document(
            m.chat.id,
            filename,
            caption="Carbon Made by: @TelePyroBot",
            reply_to_message_id=ReplyCheck(m),
        )
        await m.delete()
    else:
        await m.edit("Image Couldn't be retreived")
        await m.delete()
    os.remove(filename)
    return
