import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
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


@TelePyroBot.on_message(filters.command("sendpl", COMMAND_HAND_LER) & filters.me)
async def send_plugin(c: TelePyroBot, m: Message):
    if len(m.text.split(" ")) == 1:
        await m.edit_text("`Please enter a valid plugin name!!`")
        return
    await m.edit_text("`Sending plugin...`")
    plugin_name = m.text.split(None, 1)[1]
    if plugin_name not in ALL_PLUGINS:
        await m.edit_text(
            f"Please enter a valid plugin name!\nCheck availabe plugins by `{COMMAND_HAND_LER}plugins`."
        )
        return
    await m.reply_document(
        document=f"/root/telepyrobot/plugins/{plugin_name}.py",
        caption=f"**Plugin:** `{plugin_name}.py`\n**Plugin for** @TelePyroBot",
        disable_notification=True,
        reply_to_message_id=ReplyCheck(m),
    )
    await m.delete()
    return


@TelePyroBot.on_message(filters.command("installpl", COMMAND_HAND_LER) & filters.me)
async def install_plugin(c: TelePyroBot, m: Message):
    if len(m.command) == 1 and m.reply_to_message.document:
        if m.reply_to_message.document.file_name.split(".")[-1] != "py":
            await m.edit_text("`Can only install python (.py) files!`")
            return
        plugin_loc = (
            f"/root/telepyrobot/plugins/{m.reply_to_message.document.file_name}"
        )
        await m.edit_text("`Installing plugin...`")
        if os.path.exists(plugin_loc):
            await m.edit_text(
                f"`Plugin <i>{m.reply_to_message.document.file_name}</i> already exists!`"
            )
            return
        try:
            plugin_dl_loc = await c.download_media(
                message=m.reply_to_message, file_name=plugin_loc
            )
            if plugin_dl_loc:
                await m.edit_text(
                    f"**Installed plugin:** {m.reply_to_message.document.file_name}"
                )
        except Exception as e_f:
            await m.edit_text(f"**Error:**\n`{e_f}`")
    return


@TelePyroBot.on_message(filters.command("delpl", COMMAND_HAND_LER) & filters.me)
async def delete_plugin(c: TelePyroBot, m: Message):
    if len(m.command) == 2:
        plugin_loc = f"/root/telepyrobot/plugins/{m.command[1]}.py"
        if os.path.exists(plugin_loc):
            os.remove(plugin_loc)
            await m.edit_text(f"**Deleted plugin:** {m.command[1]}")
            return
        await m.edit_text("`Plugin does not exist!`")
        return
    await m.edit_text("`Enter a valid plugin name!`")
    return
