import os
import time
from telegraph import upload_file
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter

@Client.on_message(Filters.command("telegraph", COMMAND_HAND_LER) & sudo_filter)
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.edit("reply to a supported media file")
        return
    if not ((replied.photo and replied.photo.file_size <= 5242880)
            or (replied.animation and replied.animation.file_size <= 5242880)
            or (replied.video and replied.video.file_name.endswith('.mp4')
                and replied.video.file_size <= 5242880)
            or (replied.document
                and replied.document.file_name.endswith(
                    ('.jpg', '.jpeg', '.png', '.gif', '.mp4'))
                and replied.document.file_size <= 5242880)):
        await message.edit("**Not supported!**", parse_mode="md")
        return
    download_location = await client.download_media(message=message.reply_to_message,file_name='root/nana/')
    await message.edit("`Passing to telegraph...`", parse_mode="md")
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.edit(document)
    else:
        await message.edit(f"**Document passed to: [Telegra.ph](https://telegra.ph{response[0]})**", parse_mode="md")
    finally:
        os.remove(download_location)
