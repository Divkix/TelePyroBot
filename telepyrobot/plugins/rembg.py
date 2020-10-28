import os
from asyncio import sleep
import shutil
from removebg import RemoveBg
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, REMBG_API_KEY
from telepyrobot.utils.pyrohelpers import ReplyCheck

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__HELP__ = f"""
Use this remove background from images!

**Usage:**
`{COMMAND_HAND_LER}rembg` as a reply to photo to get it's removed bg version
"""


@TelePyroBot.on_message(filters.me & filters.command("rembg", COMMAND_HAND_LER))
async def remove_bg(c: TelePyroBot, m: Message):
    if not REMBG_API_KEY:
        await m.edit(
            "Get the API from [Remove.bg](https://www.remove.bg/api)",
            disable_web_page_preview=True,
            parse_mode="html",
        )
        return
    replied = m.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        if os.path.exists("./downloads/img.jpg"):
            os.remove("./downloads/img.jpg")
        orig_pic = await c.download_media(
            message=replied, file_name="./downloads/img.jpg"
        )
        await m.edit("`Removing Background...`")
        try:
            rmbg = RemoveBg(REMBG_API_KEY, "rembg_error.log")
            rmbg.remove_background_from_img_file(orig_pic)
            remove_img = orig_pic + "_no_bg.png"
            new_rembg_file = orig_pic.replace(".jpg", "_rembg_telepyrobot.png")
            shutil.move(remove_img, new_rembg_file)
            await c.send_document(
                chat_id=m.chat.id,
                document=new_rembg_file,
                caption="Background removed using @TelePyroBot",
                reply_to_message_id=ReplyCheck(replied),
                disable_notification=True,
            )
            await m.delete()
            os.remove(new_rembg_file)
            os.remove(orig_pic)
        except Exception as ef:
            await m.edit(f"**Error:**\n\n`{ef}")
    return
