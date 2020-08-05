import os
from asyncio import sleep

from removebg import RemoveBg
from pyrogram import Filters, Client
from pyrobot import COMMAND_HAND_LER, REMBG_API_KEY
from pyrobot.utils.pyrohelpers import ReplyCheck

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__HELP__ = f"""
Use this remove background from images!

**Usage:**
`{COMMAND_HAND_LER}rembg` as a reply to photo to get it's removed bg version
"""


DOWN_PATH = 'pyrobot/downloads/'
IMG_PATH = DOWN_PATH + "rembg_img.jpg"

@Client.on_message(Filters.me & Filters.command("rembg", COMMAND_HAND_LER))
async def remove_bg(client, message):
    if not REMBG_API_KEY:
        await message.edit("Get the API from [Remove.bg](https://www.remove.bg/b/background-removal-api)",
                           disable_web_page_preview=True, parse_mode="html")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)
        await client.download_media(message=replied, file_name=IMG_PATH)
        await message.edit("`Removing Background...`")
        try:
            rmbg = RemoveBg(REMBG_API_KEY, "rembg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            remove_img = IMG_PATH + "_no_bg.png"
            await client.send_document(
                chat_id=message.chat.id,
                document=remove_img,
                reply_to_message_id=ReplyCheck(message),
                disable_notification=True)
            await message.delete()
            os.remove(remove_img)
            os.remove(IMG_PATH)
        except Exception as e:
            print(e)
            await message.edit("`Something went wrong!`")
            await sleep(3)
            await message.delete()
    return
