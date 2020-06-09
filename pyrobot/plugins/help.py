from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

HELP_DEFAULT = f"""
To get help for any command, just type `{COMMAND_HAND_LER}help plugin_name`
Still WIP, not all Commands added.
"""

@Client.on_message(Filters.command("help", COMMAND_HAND_LER) & Filters.me)
async def help_me(client, message):
    await message.edit(HELP)
