import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.plugins import ALL_PLUGINS
from pyrobot.pyrobot import HELP_COMMANDS
from pyrobot.utils.pyrohelpers import ReplyCheck

HELP_DEFAULT = f"""
Used to install, delete or send plugins from userbot local storage!

**Usage**
`{COMMAND_HAND_LER}sendpl <plugin name>` to send a plugin
`{COMMAND_HAND_LER}installpl` as a reply to a valid plugin
`{COMMAND_HAND_LER}dlpl <plugin name>` to delete a plugin
"""


@Client.on_message(Filters.command("sendpl", COMMAND_HAND_LER) & Filters.me)
async def send_plugin(client, message):
    if len(message.text.split(" ")) == 1:
        await message.edit("`Please enter a valid plugin name!!`")
        return
    await message.edit("`Sending plugin...`")
    plugin_name = message.text.split(" ",1)[1]
    if plugin_name not in ALL_PLUGINS:
        await message.edit(f"Please enter a valid plugin name!\nCheck availabe plugins by `{COMMAND_HAND_LER}plugins`.")
        return
    await message.reply_document(
                document=f"/app/pyrobot/plugins/{plugin_name}.py",
                caption=f"**Plugin:** `{plugin_name}.py`\n**Plugin for** @TelePyroBot",
                disable_notification=True,
                reply_to_message_id=ReplyCheck(message))
    await message.delete()
    return


@Client.on_message(Filters.command("installpl", COMMAND_HAND_LER) & Filters.me)
async def install_plugin(client, message):
    if len(message.command) == 1 and message.reply_to_message.document:
        if message.reply_to_message.document.file_name.split(".")[-1] != "py":
            await message.edit("`Can only install python files!`")
            return
        plugin_loc = f"/app/pyrobot/plugins/{message.reply_to_message.document.file_name}"
        await message.edit("`Installing plugin...`")
        if os.path.exists(plugin_loc):
            await message.edit(f"`Plugin {message.reply_to_message.document.file_name.replace(".py", "")} already exists!`")
            return
        try:
            plugin_dl_loc = await client.download_media(
                message=message.reply_to_message,
                file_name=plugin_loc)
            if plugin_dl_loc:
                await message.edit(f"**Installed plugin:** {message.reply_to_message.document.file_name.replace(".py", "")}")
        except Exception as e_f:
            await message.edit(f"**Error:**\n`{e_f}`")
    return


@Client.on_message(Filters.command("delpl", COMMAND_HAND_LER) & Filters.me)
async def delete_plugin(client, message):
    if len(message.command) == 2:
        plugin_loc = f"/app/pyrobot/plugins/{message.command[1]}.py"
        if os.path.exists(plugin_loc):
            os.remove(plugin_loc)
            await message.edit(f"**Deleted plugin:** {message.command[1]}")
            return
        await message.edit("`Plugin does not exist!`")
        return
    await message.edit("`Enter a valid plugin name!`")
    return