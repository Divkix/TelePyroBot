import os
import time
import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}sdd <link>`

The command will download the song from specified link and send to you.
"""

@Client.on_message(Filters.command("sdd", COMMAND_HAND_LER) & Filters.me)
async def sd_downloader(client, message):
    if len(message.command) == 2:
        song_link = message.text.split(" ",1)[1]
    elif message.reply_to_message:
        song_link = message.reply_to_message.text
    await client.send_message("@DeezLoadBot", f"{song_link}")
    await message.edit(f"`Please wait <u>5</u> seconds.`")
    time.sleep(4)
    msg = await client.get_history("@DeezLoadBot", limit=3)
    msg_id = msg[1]["audio"]["message_id"]
    try:
        await client.forward_messages(message.chat.id, "@DeezLoadBot", msg_id)
    except:
        await message.reply_text("`Not able to fetch music :^(`")
    await client.read_history("@DeezLoadBot")
    await message.delete()
