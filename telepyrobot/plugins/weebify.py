import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Get information about a Github Account
Usage: `{COMMAND_HAND_LER}weebify <text>` or a reply to message to weebify the message.
"""

normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]


@TelePyroBot.on_message(filters.command("weebify", COMMAND_HAND_LER) & filters.me)
async def weebify(c: TelePyroBot, m: Message):
    if len(m.command) >= 2:
        args = m.text.split(" ", 1)[1]
    if m.reply_to_message and len(m.command) == 1:
        args = m.reply_to_m.text
    if not args:
        await event.edit("`What I am Supposed to Weebify dumb`")
        return
    string = "  ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await m.edit(f"**Weebified String:**\n`{string}`")
    return
