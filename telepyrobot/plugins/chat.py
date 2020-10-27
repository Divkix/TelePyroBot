import os
import asyncio
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from telepyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN
from telepyrobot.utils.admin_check import admin_check

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


@TelePyroBot.on_message(filters.command("leavechat", COMMAND_HAND_LER) & filters.me)
async def leavechat(c: TelePyroBot, m: Message):
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.leave_chat(chat_id, delete=True)


@TelePyroBot.on_message(filters.command("invitelink", COMMAND_HAND_LER) & filters.me)
async def invitelink(c: TelePyroBot, m: Message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    link = await client.export_chat_invite_link(chat_id)
    await m.edit(f"**Link for Chat:**\n`{link}`")


@TelePyroBot.on_message(filters.command("setchatpic", COMMAND_HAND_LER) & filters.me)
async def set_picture(c: TelePyroBot, m: Message):
    if message.chat.type in ["group", "supergroup"]:
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await m.edit("`Tring to Change Group Picture....`")
        chat_id = message.chat.id
        try:
            if m.reply_to_message and m.reply_to_message.media:
                file_id = m.reply_to_message.photo.file_id
                file_ref = m.reply_to_message.photo.file_ref
                await client.set_chat_photo(chat_id, file_id, file_ref=file_ref)
                await m.edit(f"`{message.chat.type.title()} picture has been set.`")
            else:
                await m.edit("`Reply to an image to set that as group pic`")
        except Exception as ef:
            await m.edit(f"**Could not Change Chat Pic due to:**\n`{ef}`")


@TelePyroBot.on_message(filters.command("delchatpic", COMMAND_HAND_LER) & filters.me)
async def delchatpic(c: TelePyroBot, m: Message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    try:
        await client.delete_chat_photo(chat_id)
        await m.edit(f"`Deleted Chat Picture for {message.chat.type.title()}`")
    except Exception as ef:
        await m.edit(f"Error deleting Chat Pic due to:\n`{ef}`")


@TelePyroBot.on_message(filters.command("setchatname", COMMAND_HAND_LER) & filters.me)
async def setchatname(c: TelePyroBot, m: Message):
    await m.edit("__Trying to Change Chat Name!__")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    chat_title = message.text.split(" ", 1)
    if m.reply_to_message:
        chat_title = m.reply_to_message.text
    else:
        chat_title = chat_title[1]
    try:
        await client.set_chat_title(chat_id, chat_title)
        await m.edit(f"<b>Changed Chat Name to:</b> <code>{chat_title}</code>")
    except Exception as ef:
        await m.edit(f"**Could not Change Chat Title due to:**\n`{ef}`")


@TelePyroBot.on_message(filters.command("setchatdesc", COMMAND_HAND_LER) & filters.me)
async def setchatdesc(c: TelePyroBot, m: Message):
    await m.edit("__Trying to Change Chat Desciption!__")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    chat_desc = message.text.split(" ", 1)
    if m.reply_to_message:
        chat_desc = m.reply_to_message.text
    else:
        chat_desc = chat_desc[1]
    try:
        await client.set_chat_description(chat_id, chat_desc)
        await m.edit(f"<b>Changed Chat Description to:</b> <code>{chat_desc}</code>")
    except Exception as ef:
        await m.edit(f"**Could not Change Chat Desciption due to:**\n`{ef}`")
