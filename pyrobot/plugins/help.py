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

HELP_DEFAULT = f"""
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
    for modul in ALL_PLUGINS:
        mods += f"`{modul}`\n"
        mod_num += 1
    all_plugins = f"<b><u>{mod_num}</u> Modules Currently Loaded:</b>\n\n" + mods
    await message.edit(all_plugins)


@Client.on_message(Filters.command("help", COMMAND_HAND_LER) & Filters.me)
async def help_me(client, message):
    if len(message.command) == 1:
        await message.edit(HELP_DEFAULT)
    elif len(message.command) == 2:
        module_name = message.command[1]
        try:
            await message.edit(HELP_COMMANDS['module_name'])
        except Exception as ef:
            await message.edit(f"<b>Error:</b>\n\n{ef}")
