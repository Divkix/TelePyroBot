import io
import os
import sys
import traceback
import time
import asyncio
import requests
from pyrogram import Client, Filters
from pyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER, ALL_MODULES

HELP_DEFAULT = f"""
To get help for any command, just type `{COMMAND_HAND_LER}help plugin_name`
Still WIP, not all Commands added.
"""

@Client.on_message(Filters.command("plugins", COMMAND_HAND_LER) & Filters.me)
async def execution(client, message):
    #Some Variables
    mods = ""
    mod_num = 0
    #Some Variables
    for modul in ALL_MODULES:
        mods += f"{modul}\n"
        mod_num += 1
    all_plugins = f"**{mod_num}** Modules Currently Loaded:\n\n" + mods
    await message.edit(all_plugins)

@Client.on_message(Filters.command("help", COMMAND_HAND_LER) & Filters.me)
async def help_me(client, message):
    await message.edit(HELP)
