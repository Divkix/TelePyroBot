import io
import os
import sys
import traceback
import time
import asyncio
import requests
from pyrogram import Client, Filters
from pyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER
from pyrobot.plugins import ALL_PLUGINS
from pyrobot.pyrobot import HELP_COMMANDS

__PLUGIN__ = "HELP"

__help__ = f"""
To get help for any command, just type `{COMMAND_HAND_LER}help plugin_name`

List of all Plugins: `{COMMAND_HAND_LER}plugins`

<b>Still WIP, not all Commands added!</b>
"""

@Client.on_message(Filters.command("plugins", COMMAND_HAND_LER) & Filters.me)
async def execution(client, message):
    #Some Variables
    mods = ""
    mod_num = 0
    #Some Variables
    plugins = list(HELP_COMMANDS.keys())
    for plug in plugins:
        mods += f"`{plug}`\n"
        mod_num += 1
    all_plugins = f"<b><u>{mod_num}</u> Modules Currently Loaded:</b>\n\n" + mods
    await message.edit(all_plugins)


@Client.on_message(Filters.command("help", COMMAND_HAND_LER) & Filters.me)
async def help_me(client, message):
    if len(message.command) == 1:
        await message.edit(HELP_DEFAULT)
    elif len(message.command) == 2:
        module_name = message.text.split(" ",1)[1]
        try:
            await message.reply_text(HELP_COMMANDS.get[f'{module_name}'])
            await message.delete()
        except Exception as ef:
            await message.edit(f"<b>Error:</b>\n\n{ef}")
