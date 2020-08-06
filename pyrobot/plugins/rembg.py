import os
from asyncio import sleep
import shutil
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


@Client.on_message(Filters.me & Filters.command("rembg", COMMAND_HAND_LER))
async def remove_bg(client, message):
    if not REMBG_API_KEY:
        await message.edit("Get the API from [Remove.bg](https://www.remove.bg/api)",
                           disable_web_page_preview=True, parse_mode="html")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        if os.path.exists("./downloads/img.jpg"):
            os.remove("./downloads/img.jpg")
        orig_pic = await client.download_media(message=replied, file_name="./downloads/img.jpg")
        await message.edit("`Removing Background...`")
        try:
            rmbg = RemoveBg(REMBG_API_KEY, "rembg_error.log")
            rmbg.remove_background_from_img_file(orig_pic)
            remove_img = orig_pic + "_no_bg.png"
            new_rembg_file = orig_pic.replace(".jpg", "_rembg_telepyrobot.png")
            shutil.move(remove_img, new_rembg_file)
            await client.send_document(
                chat_id=message.chat.id,
                document=new_rembg_file,
                caption="Background removed using @TelePyroBot",
                reply_to_message_id=ReplyCheck(message),
                disable_notification=True)
            await message.delete()
            os.remove(new_rembg_file)
            os.remove(orig_pic)
        except Exception as ef:
            await message.edit(f"**Error:**\n\n`{ef}")
    return
