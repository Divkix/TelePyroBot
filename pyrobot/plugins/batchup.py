import os
import time
import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY, LOGGER
from pyrobot.utils.display_progress_dl_up import (
    progress_for_pyrogram,
    humanbytes
)
from pyrobot.utils.check_if_thumb_exists import is_thumb_image_exists
from pyrobot.utils.display_progress_dl_up import progress_for_pyrogram

__PLUGIN__ = __file__.replace(".py", "")

__help__ = f"""
Upload files from a directory to telegram easily!
Usage: {COMMAND_HAND_LER}batchup <directory location>

The command will upload all files from the directory location to Telegram Chat.
"""

@Client.on_message(Filters.command("batchup", COMMAND_HAND_LER) & Filters.me)
async def covid(client, message):
    if len(message.command) == 1:
        await message.edit("Enter a directory location")
    elif len(message.command) == 2:
        temp_dir = message.text.split(" ", 1)[1]
    else:
        await message.edit(f"Please check help by using `{COMMAND_HAND_LER}help batchup`")
    status_message = await message.reply_text("`Uploading Files...`")
    if os.path.exists(temp_dir):
        files = os.listdir(temp_dir)
        files.sort()
        await status_message.edit("Uploading Files on Telegram...")
        for file in files:
            c_time = time.time()
            required_file_name = temp_dir+"/"+file
            thumb_image_path = await is_thumb_image_exists(required_file_name)
            doc_caption = os.path.basename(required_file_name)
            LOGGER.info(f"Uploading {required_file_name}")
            await message.reply_document(
                document=required_file_name,
                thumb=thumb_image_path,
                caption=doc_caption,
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload", status_message, c_time)
                )
    else:
        await message.edit("Directory Not Found.")
        return
    await client.send_message(message.chat.id, "Successfull.")
