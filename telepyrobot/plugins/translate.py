from googletrans import Translator
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
import os
from telepyrobot import COMMAND_HAND_LER

trl = Translator()


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))
__help__ = f"""
**Translate**
`{COMMAND_HAND_LER}tr <lang> <text>`
Give a target language and text as args for translate to that target.
Reply a message to translate that.

*text is not uaed when replying to a message
"""


@TelePyroBot.on_message(filters.me & filters.command("tr", COMMAND_HAND_LER))
async def translate(c: TelePyroBot, m: Message):
    if m.reply_to_message and (m.reply_to_m.text or m.reply_to_message.caption):
        if len(m.text.split()) == 1:
            await m.edit("Usage: Reply to a message, then `tr <lang>`")
            return
        target = m.text.split()[1]
        if m.reply_to_m.text:
            text = m.reply_to_m.text
        else:
            text = m.reply_to_message.caption
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await m.edit(f"Error: `{str(err)}`")
            return
    else:
        if len(m.text.split()) <= 2:
            await m.edit("Usage: `tr <lang> <text>`")
            return
        target = m.text.split(None, 2)[1]
        text = m.text.split(None, 2)[2]
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await m.edit("Error: `{}`".format(str(err)))
            return

    await m.edit(f"Translated from `{detectlang.lang}` to `{target}`:\n`{tekstr.text}`")
    return
