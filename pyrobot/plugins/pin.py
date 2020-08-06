import os
import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
from pyrobot.utils.admin_check import admin_check

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Plugin to help you pin or unpin messages in a group!

`{COMMAND_HAND_LER}pin`: Pins the message in the Group.
`{COMMAND_HAND_LER}unpin`: unpins the message in the Group.
"""


@Client.on_message(Filters.command("pin", COMMAND_HAND_LER) & Filters.me)
async def pin_message(client, message):
    if PRIVATE_GROUP_ID is None:
        await message.edit("Please set `PRIVATE_GROUP_ID` variable to make me work!")
        return
    if message.chat.type in ['group', 'supergroup']:
        await message.edit("`Trying to pin message...`")
        is_admin = await admin_check(message)
        if not is_admin:
            await msg.edit("`I'm not admin nub nibba!`")
            await asyncio.sleep(2)
            await message.delete()
            return
        pin_loud = message.text.split(' ', 1)
        if message.reply_to_message:
            disable_notification = True

            if len(pin_loud) >= 2 and pin_loud[1] in ['alert', 'notify', 'loud']:
                disable_notification = False

            pinned_event = await client.pin_chat_message(
                message.chat.id,
                message.reply_to_message.message_id,
                disable_notification=disable_notification)
            await message.edit("`Pinned message!`")
        else:
            await message.edit("`Reply to a message to which you want to pin...`")
    await client.send_message(
        PRIVATE_GROUP_ID,
        f"#PIN\n\nPinned message in **{message.chat.title}**")
    return


@Client.on_message(Filters.command("unpin", COMMAND_HAND_LER) & Filters.me)
async def unpin_message(client, message):
    if PRIVATE_GROUP_ID is None:
        await message.edit("Please set `PRIVATE_GROUP_ID` variable to make me work!")
        return
    if message.chat.type in ['group', 'supergroup']:
        await message.edit("`Trying to unpin message...`")
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.unpin_chat_message(chat_id)
        await message.edit("`Unpinned message!`")
        await client.send_message(
            PRIVATE_GROUP_ID,
            f"#UNPIN\\n\nUnpinned message in **{message.chat.title}**")
        await asyncio.sleep(3)
        await message.delete()
        return
