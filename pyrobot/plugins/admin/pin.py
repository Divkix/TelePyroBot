import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot.helper_functions.admin_check import admin_check

@Client.on_message(Filters.command("pin", COMMAND_HAND_LER) & sudo_filter)
async def pin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        is_admin = await admin_check(message)
        if not is_admin:
            return

        if message.reply_to_message:
            disable_notification = True

            if len(message.command) >= 2 and message.command[1] in ['alert', 'notify', 'loud']:
                disable_notification = False

            pinned_event = await client.pin_chat_message(
                message.chat.id,
                message.reply_to_message.message_id,
                disable_notification=disable_notification
            )
            await message.reply_text("`Pinned message!`", parse_mode="md")
            return
        else:
            await message.reply_text(
                f"`Reply to a message so that I can pin the god damned thing...`", parse_mode="md")
    await asyncio.sleep(3)
    await message.delete()

@Client.on_message(Filters.command("unpin", COMMAND_HAND_LER) & sudo_filter)
async def unpin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.unpin_chat_message(chat_id)
        await message.reply_text("`Unpinned message!`", parse_mode="md")
        await asyncio.sleep(3)
        await message.delete()
