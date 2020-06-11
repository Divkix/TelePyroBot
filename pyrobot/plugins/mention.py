import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Generate a  hyperlink username you refer with a custom single text.

──「 **Mention** 」──
Usage: `{COMMAND_HAND_LER}mention <username without @> <custom text>`
"""

@Client.on_message(Filters.command("mention", COMMAND_HAND_LER) & Filters.me)
async def mention(_, message):
    args = message.text.split(None, 2)
    if len(args) == 3:
        user = args[1]
        name = args[2]
        rep = f'<a href="tg://resolve?domain={user}">{name}</a>'
        await message.edit(
            rep,
            disable_web_page_preview=True,
            parse_mode="html")
    else:
        await message.edit(f"**Usage:** `{COMMAND_HAND_LER}mention <username without @> <custom text>`", parse_mode="md")
        return
