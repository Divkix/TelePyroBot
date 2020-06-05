from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter
import random
import time

@Client.on_message(Filters.command("qbot", COMMAND_HAND_LER) & sudo_filter)
async def quotly(client, message):
    if not message.reply_to_message:
        await message.edit("Reply to any users text message")
        return
    await message.edit("```Making a Quote```")
    await message.reply_to_message.forward("@QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            msg = await app.get_history("@QuotLyBot", 1)
            check = msg[0]["sticker"]["file_id"]
            is_sticker = True
        except:
            time.sleep(0.5)
            progress += random.randint(0, 10)
            try:
                await message.edit("```Making a Quote```\nProcessing {}%".format(progress))
            except:
                await message.edit("ERROR SUUUU")
    await message.edit("```Complete !```")
    msg_id = msg[0]["message_id"]
    await app.forward_messages(message.chat.id, "@QuotLyBot", msg_id)
