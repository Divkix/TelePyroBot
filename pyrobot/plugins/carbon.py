from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.cust_p_filters import sudo_filter
from pyrobot.utils.list_to_string import listToString
from requests import post
import shutil
import os
from time import sleep

CARBON_LANG = "Auto"

@Client.on_message(Filters.command("carbon", COMMAND_HAND_LER) & sudo_filter)
async def carbon_api(client, message):
    json = {
        "backgroundColor": "rgba(0, 255, 230, 100)",
        "theme": "Dracula",
        "exportSize": "4x"
        }
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
        r = message.reply_to_message
        json["code"] = r.text
        await message.edit_text("Carbonizing code...")
    if len(message.command) >= 2:
        r = message.command[1:]
        json["code"] = listToString(r)
    else:
        await message.edit("Usage: `.carbon` (reply to a code or text)")
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
