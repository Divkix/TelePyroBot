import os
import asyncio
from pyrogram import Client, Filters, ChatPermissions
from pyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN
from pyrobot.utils.admin_check import admin_check

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Commands to help you manage a chat.

`{COMMAND_HAND_LER}leavechat`: Exit from the Group.
Usage: {COMMAND_HAND_LER}leavechat

`{COMMAND_HAND_LER}invitelink`: Gives the invitelink of the Group.
Usage: {COMMAND_HAND_LER}invitelink

`{COMMAND_HAND_LER}setchatpic`: Changes the Picture of Group.
Usage: {COMMAND_HAND_LER}setchatpic (as a reply to the message)

`{COMMAND_HAND_LER}delchatpic`: Removes the Picture of Group.
Usage: {COMMAND_HAND_LER}delchatpic (as a reply to the message)

`{COMMAND_HAND_LER}setchatname`: Renames the Group.
Usage: {COMMAND_HAND_LER}setchatname (chatname or as a reply to the message)

`{COMMAND_HAND_LER}setchatdesc`: Sets the Description of the Group.
Usage: {COMMAND_HAND_LER}setchatdesc (chatdesc or as a reply to the message)
"""

@Client.on_message(Filters.command("leavechat", COMMAND_HAND_LER) & Filters.me)
async def leavechat(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.leave_chat(chat_id, delete=True)


@Client.on_message(Filters.command("invitelink", COMMAND_HAND_LER) & Filters.me)
async def invitelink(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    link = await client.export_chat_invite_link(chat_id)
    await message.edit(f"**Link for Chat:**\n`{link}`")


@Client.on_message(Filters.command("setchatpic", COMMAND_HAND_LER) & Filters.me)
async def set_picture(client, message):
    if message.chat.type in ['group', 'supergroup']:
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await message.edit("`Tring to Change Group Picture....`")
        chat_id = message.chat.id
        try:
            if message.reply_to_message and message.reply_to_message.media:
                file_id = message.reply_to_message.photo.file_id
                file_ref = message.reply_to_message.photo.file_ref
                await client.set_chat_photo(chat_id, file_id, file_ref=file_ref)
                await message.edit(f"`{message.chat.type.title()} picture has been set.`")
            else:
                await message.edit("`Reply to an image to set that as group pic`")
        except Exception as ef:
            await message.edit(f"**Could not Change Chat Pic due to:**\n`{ef}`")


@Client.on_message(Filters.command("delchatpic", COMMAND_HAND_LER) & Filters.me)
async def delchatpic(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    try:
        await client.delete_chat_photo(chat_id)
        await message.edit(f"`Deleted Chat Picture for {message.chat.type.title()}`")
    except Exception as ef:
        await message.edit(f"Error deleting Chat Pic due to:\n`{ef}`")


@Client.on_message(Filters.command("setchatname", COMMAND_HAND_LER) & Filters.me)
async def setchatname(client, message):
    await message.edit("__Trying to Change Chat Name!__")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    chat_title = message.text.split(' ', 1)
    if message.reply_to_message:
        chat_title = message.reply_to_message.text
    else:
        chat_title = chat_title[1]
    try:
        await client.set_chat_title(chat_id, chat_title)
        await message.edit(f"<b>Changed Chat Name to:</b> <code>{chat_title}</code>")
    except Exception as ef:
        await message.edit(f"**Could not Change Chat Title due to:**\n`{ef}`")


@Client.on_message(Filters.command("setchatdesc", COMMAND_HAND_LER) & Filters.me)
async def setchatdesc(client, message):
    await message.edit("__Trying to Change Chat Desciption!__")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    chat_desc = message.text.split(' ', 1)
    if message.reply_to_message:
        chat_desc = message.reply_to_message.text
    else:
        chat_desc = chat_desc[1]
    try:
        await client.set_chat_description(chat_id, chat_desc)
        await message.edit(f"<b>Changed Chat Description to:</b> <code>{chat_desc}</code>")
    except Exception as ef:
        await message.edit(f"**Could not Change Chat Desciption due to:**\n`{ef}`")
