import os
from pyrogram import Client, filters
from telepyrobot import COMMAND_HAND_LER
from pyrogram.types import Message
from telepyrobot.plugins import ALL_PLUGINS
from telepyrobot.utils.pyrohelpers import ReplyCheck

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Used to install, delete or send plugins from userbot local storage!

**Usage**
`{COMMAND_HAND_LER}sendpl <plugin name>` to send a plugin
`{COMMAND_HAND_LER}installpl` as a reply to a valid plugin
`{COMMAND_HAND_LER}delpl <plugin name>` to delete a plugin
"""


@Client.on_message(filters.command("sendpl", COMMAND_HAND_LER) & filters.me)
async def send_plugin(c: Client, m: Message):
    if len(message.text.split(" ")) == 1:
        await m.edit("`Please enter a valid plugin name!!`")
        return
    await m.edit("`Sending plugin...`")
    plugin_name = message.text.split(" ", 1)[1]
    if plugin_name not in ALL_PLUGINS:
        await m.edit(
            f"Please enter a valid plugin name!\nCheck availabe plugins by `{COMMAND_HAND_LER}plugins`."
        )
        return
    await message.reply_document(
        document=f"/app/telepyrobot/plugins/{plugin_name}.py",
        caption=f"**Plugin:** `{plugin_name}.py`\n**Plugin for** @TelePyroBot",
        disable_notification=True,
        reply_to_message_id=ReplyCheck(message),
    )
    await m.delete()
    return


@Client.on_message(filters.command("installpl", COMMAND_HAND_LER) & filters.me)
async def install_plugin(c: Client, m: Message):
    if len(message.command) == 1 and m.reply_to_message.document:
        if m.reply_to_message.document.file_name.split(".")[-1] != "py":
            await m.edit("`Can only install python files!`")
            return
        plugin_loc = f"/app/telepyrobot/plugins/{m.reply_to_message.document.file_name}"
        await m.edit("`Installing plugin...`")
        if os.path.exists(plugin_loc):
            await m.edit(
                f"`Plugin {m.reply_to_message.document.file_name} already exists!`"
            )
            return
        try:
            plugin_dl_loc = await client.download_media(
                message=m.reply_to_message, file_name=plugin_loc
            )
            if plugin_dl_loc:
                await m.edit(
                    f"**Installed plugin:** {m.reply_to_message.document.file_name}"
                )
        except Exception as e_f:
            await m.edit(f"**Error:**\n`{e_f}`")
    return


@Client.on_message(filters.command("delpl", COMMAND_HAND_LER) & filters.me)
async def delete_plugin(c: Client, m: Message):
    if len(message.command) == 2:
        plugin_loc = f"/app/telepyrobot/plugins/{message.command[1]}.py"
        if os.path.exists(plugin_loc):
            os.remove(plugin_loc)
            await m.edit(f"**Deleted plugin:** {message.command[1]}")
            return
        await m.edit("`Plugin does not exist!`")
        return
    await m.edit("`Enter a valid plugin name!`")
    return
