from googletrans import Translator
from pyrogram import filters, Client
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


@Client.on_message(filters.me & filters.command("tr", COMMAND_HAND_LER))
async def translate(client, message):
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        if len(message.text.split()) == 1:
            await message.edit("Usage: Reply to a message, then `tr <lang>`")
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await message.edit(f"Error: `{str(err)}`")
            return
    else:
        if len(message.text.split()) <= 2:
            await message.edit("Usage: `tr <lang> <text>`")
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await message.edit("Error: `{}`".format(str(err)))
            return

    await message.edit(
        f"Translated from `{detectlang.lang}` to `{target}`:\n`{tekstr.text}`"
    )
    return
