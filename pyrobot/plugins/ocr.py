from pyrogram import Client, Filters
import os
from pyrobot import COMMAND_HAND_LER
import asyncio
import time

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Convert Image to text easily!

`{COMMAND_HAND_LER}ocrimg`: As a reply to message to get its text.
"""

@Client.on_message(Filters.command("ocrimg", COMMAND_HAND_LER) & Filters.me)
async def ocr_img(client, message):
    if not message.reply_to_message:
        await message.edit("Reply to any users text message")
        return
    await message.edit("`Finding text in Image...`", parse_mode="md")
    await message.reply_to_message.forward("@imagereaderbot")
    await asyncio.sleep(3)
    msg = await client.get_history("@imagereaderbot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@imagereaderbot", msg_id)
    await client.read_history("@imagereaderbot")
    await message.delete()
