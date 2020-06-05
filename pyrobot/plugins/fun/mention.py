"""
──「 **Mention** 」──
-> `mention (username without @) (custom text)`
Generate a  hyperlink username you refer with a custom single text.
"""

from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter

@Client.on_message(Filters.command("mention", COMMAND_HAND_LER) & sudo_filter)
async def mention(_, message):
    args = message.text.split(None, 2)
    if len(args) == 3:
        user = args[1]
        name = args[2]
        rep = f'<a href="tg://resolve?domain={user}">{name}</a>'
        await message.edit(
            rep,
            disable_web_page_preview=True,
            parse_mode="html"
        )
    else:
        await message.edit("Usage: `mention (username without @) (custom text)`")
        return
