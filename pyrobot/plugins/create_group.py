import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, LOGGER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Create groups easily with userbot!
Syntax: `{COMMAND_HAND_LER}creategrp <type> <name>`

Commands:
`{COMMAND_HAND_LER}creategrp super <name of new group>` will make a supergroup.
`{COMMAND_HAND_LER}creategrp basic <name of new group>` will make a basic group.
"""

@Client.on_message(Filters.command("creategrp", COMMAND_HAND_LER) & Filters.me)
async def cas(client, message):
    if len(message.command) < 3:
        await message.edit("`Check help, you don't know how to use it`")
        return

    args = message.text.split(" ", 2)
    grpname =  args[2]
    grptype = args[1]
    user_id = "@Alita_Robot"

    if grptype == "basic":
        try:
            await message.edit(f"__Trying to make a BasicGroup named:__`{grpname}`")
            await client.create_group(f"{grpname}", user_id)
        except Exception as ef:
            await message.edit(f"**Error:**\n`{ef}`")
            return

    elif grptype == "super":
        try:
            await message.edit(f"__Trying to make a SuperGroup named:__`{grpname}`")
            await client.create_supergroup(f"{grpname}")
        except Exception as ef:
            await message.edit(f"**Error:**\n`{ef}`")
            return
