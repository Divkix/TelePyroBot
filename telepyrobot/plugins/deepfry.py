import io
import os
import asyncio
from random import randint, uniform
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.msg_types import Types
from telepyrobot.utils.pyrohelpers import extract_user
from PIL import Image, ImageEnhance, ImageOps


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Burn media files and make them look sick!

**Commands:**
`{COMMAND_HAND_LER}deepfry` as a reply to media (Sticker or photo)
"""


@TelePyroBot.on_message(filters.command("deepfry", COMMAND_HAND_LER) & filters.me)
async def do_deepfry(c: TelePyroBot, m: Message):
    try:
        frycount = int(m.text.split(" ", 1)[1])
        if frycount < 1:
            frycount = 1
    except IndexError:
        frycount = 1

    if m.reply_to_message.photo or m.reply_to_message.sticker:
        reply_message = m.reply_to_message
        data = await check_media(reply_message)
    else:
        await m.edit_text("`Reply to an image or sticker to deep fry it!`")
        return

    # download last photo (highres) as byte array
    await m.edit_text("`Downloading media...`")
    image = io.BytesIO()
    image = await c.download_media(data)
    image = Image.open(image)

    await asyncio.sleep(3)
    await m.edit_text("`Deep frying media...`")
    for _ in range(frycount):
        image = await deepfry(image)

    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)

    await m.reply_photo(photo=fried_io, caption="Deepfried by @TelePyroBot")
    await m.delete()
    return


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )

    img = img.copy().convert("RGB")

    # Crush image to hell and back
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))

    # Generate colour overlay
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))

    overlay = ImageOps.colorize(overlay, colours[0], colours[1])

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))

    return img


async def check_media(repl_msg):
    if repl_msg and repl_msg.media:
        if repl_msg.photo:
            data = repl_msg.photo
        elif repl_msg.sticker:
            data = repl_msg.sticker
        else:
            return False
        return data
    else:
        return False
