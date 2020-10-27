import os
import asyncio
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
from telepyrobot.utils.admin_check import admin_check

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Plugin to help you pin or unpin messages in a group!

`{COMMAND_HAND_LER}pin`: Pins the message in the Group.
`{COMMAND_HAND_LER}unpin`: unpins the message in the Group.
"""


@TelePyroBot.on_message(filters.command("pin", COMMAND_HAND_LER) & filters.me)
async def pin_message(c: Client, m: Message):
    if PRIVATE_GROUP_ID is None:
        await m.edit("Please set `PRIVATE_GROUP_ID` variable to make me work!")
        return
    if message.chat.type in ["group", "supergroup"]:
        await m.edit("`Trying to pin message...`")
        is_admin = await admin_check(message)
        if not is_admin:
            await msg.edit("`I'm not admin nub nibba!`")
            await asyncio.sleep(2)
            await m.delete()
            return
        pin_loud = message.text.split(" ", 1)
        if m.reply_to_message:
            disable_notification = True

            if len(pin_loud) >= 2 and pin_loud[1] in ["alert", "notify", "loud"]:
                disable_notification = False

            pinned_event = await client.pin_chat_message(
                message.chat.id,
                m.reply_to_message.message_id,
                disable_notification=disable_notification,
            )
            await m.edit("`Pinned message!`")
        else:
            await m.edit("`Reply to a message to which you want to pin...`")
    await c.send_message(
        PRIVATE_GROUP_ID, f"#PIN\n\nPinned message in **{message.chat.title}**"
    )
    return


@TelePyroBot.on_message(filters.command("unpin", COMMAND_HAND_LER) & filters.me)
async def unpin_message(c: Client, m: Message):
    if PRIVATE_GROUP_ID is None:
        await m.edit("Please set `PRIVATE_GROUP_ID` variable to make me work!")
        return
    if message.chat.type in ["group", "supergroup"]:
        await m.edit("`Trying to unpin message...`")
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.unpin_chat_message(chat_id)
        await m.edit("`Unpinned message!`")
        await c.send_message(
            PRIVATE_GROUP_ID, f"#UNPIN\\n\nUnpinned message in **{message.chat.title}**"
        )
        await asyncio.sleep(3)
        await m.delete()
        return
