import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.parser import mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Generate a  hyperlink/permanent link for a profile.

**Mention**
Usage:
`{COMMAND_HAND_LER}mention <custom text> <username without @>`
or
`{COMMAND_HAND_LER}mention <custom text> <user id>`
"""


@TelePyroBot.on_message(filters.command("mention", COMMAND_HAND_LER) & filters.me)
async def mention(c: TelePyroBot, m: Message):
    args = message.text.split(" ", 2)
    if len(args) == 3:
        name = args[1]
        if isinstance(args[2], int):
            user = args[2]
            rep = "{}".format(mention_markdown(name, user))
        else:
            user = args[2]
            rep = f'<a href="tg://resolve?domain={name}">{user}</a>'
        await m.edit(rep, disable_web_page_preview=True, parse_mode="html")
    else:
        await m.edit(
            f"Check `{COMMAND_HAND_LER}help {__PLUGIN__}` for infor on how to use",
            parse_mode="md",
        )
        return
