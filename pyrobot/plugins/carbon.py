from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from requests import post
import shutil
import os
from time import sleep

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ =  f"""
`{COMMAND_HAND_LER}carbon` <text> or as a reply to the message.
"""

CARBON_LANG = "Auto"

@Client.on_message(Filters.command("carbon", COMMAND_HAND_LER) & Filters.me)
async def carbon_api(client, message):
    json = {
        "backgroundColor": "rgba(0, 255, 230, 100)",
        "theme": "Dracula",
        "exportSize": "4x"
        }
    cmd = message.command
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
        r = message.reply_to_message
        json["code"] = r.text
        await message.edit_text("`Carbonizing code...`")
    if len(cmd) >= 2:
        r = message.text.split(" ", 1)[1]
        json["code"] = r
    else:
        await message.edit("Usage: `.carbon` <reply to a code or text>")
    json["language"] = CARBON_LANG
    apiUrl = "http://carbonnowsh.herokuapp.com"
    r = post(apiUrl,json=json,stream=True)
    filename = 'carbon.png'
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        await client.send_document(message.chat.id, filename, reply_to_message_id=rep_mesg_id)
        await message.delete()
    else:
        await message.edit('Image Couldn\'t be retreived')
        await message.delete()
    os.remove(filename)
