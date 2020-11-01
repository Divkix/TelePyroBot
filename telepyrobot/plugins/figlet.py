import pyfiglet
import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}figlet <text> | <font-type>`

The command send the figlet of the text you give it.

Figlet styles can be found here:
https://nekobin.com/hesoyipowo
"""


@TelePyroBot.on_message(filters.command("figlet", COMMAND_HAND_LER) & filters.me)
async def figlet_font(c: TelePyroBot, m: Message):
    CMD_FIG = {
        "slant": "slant",
        "3D": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    input_str = m.text.split(None, 1)[1]
    if "|" in input_str:
        text, font_style = input_str.split("|", maxsplit=1)
    elif input_str is not None:
        font_style = None
        text = input_str
    else:
        await m.edit_text("`Please add some text to figlet`")
        return
    if font_style is not None:
        try:
            font = CMD_FIG[font_style]
        except KeyError:
            await m.edit_text("`Font not available`")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await m.reply_text(f"‌‌‎`{result}`")
    await m.delete()
    return
