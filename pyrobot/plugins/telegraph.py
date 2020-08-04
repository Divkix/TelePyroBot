import os
import time
from datetime import datetime
from telegraph import upload_file
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}telegraph`: As a reply to a media to paste it to Telegraph.
"""

@Client.on_message(Filters.command("telegraph", COMMAND_HAND_LER) & Filters.me)
async def telegraph(client, message):
    replied = message.reply_to_message
    start_t = datetime.now()
    await message.edit("`Trying to paste to telegraph...`", parse_mode="md")
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
    download_location = await client.download_media(message=message.reply_to_message,file_name='pyrobot/downloads/')
    await message.edit("`Pasting to telegraph...`", parse_mode="md")
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.edit(document)
    else:
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await message.edit(f"**Document Passed to** [Telegra.ph](https://telegra.ph{response[0]}) **in __{ms}__ seconds**", parse_mode="md", disable_web_page_preview=True)
    finally:
        os.remove(download_location)
