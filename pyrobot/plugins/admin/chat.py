from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot.helper_functions.admin_check import admin_check


@Client.on_message(Filters.command("leavechat", COMMAND_HAND_LER) & sudo_filter)
async def leavechat(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.leave_chat(chat_id, delete=True)


@Client.on_message(Filters.command("invitelink", COMMAND_HAND_LER) & sudo_filter)
async def invitelink(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    link = client.export_chat_invite_link(chat_id)
    await message.reply_text(f"**Link for Chat:**\n`{link}`", parse_mode="md")


@Client.on_message(Filters.command("setchatpic", COMMAND_HAND_LER) & sudo_filter)
async def set_picture(client, message):
    if message.chat.type in ['group', 'supergroup']:
        is_admin = await admin_check(message)
        if not is_admin:
            return
        rm = await message.reply_text("`Tring to Change Group Picture....`", parse_mode="md")
        chat_id = message.chat.id
        try:
            if message.reply_to_message and message.reply_to_message.media:
                file_id = message.reply_to_message.photo.file_id
                file_ref = message.reply_to_message.photo.file_ref
                await client.set_chat_photo(chat_id, file_id, file_ref=file_ref)
                await rm.edit(f"`{message.chat.type.title()} picture has been set.`", parse_mode="md")
            else:
                await rm.edit("`Reply to an image to set that as group pic`", parse_mode="md")
        except Exception as ef:
            await rm.edit(f"**Could not Change Chat Pic due to:**\n`{ef}`")


@Client.on_message(Filters.command("delchatpic", COMMAND_HAND_LER) & sudo_filter)
async def delchatpic(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    try:
        await client.delete_chat_photo(chat_id)
        await message.reply_text(f"`Deleted Chat Picture for {message.chat.type.title()}`", parse_mode="md")
    except Exception as ef:
        await message.reply_text(f"Error deleting Chat Pic due to:\n`{ef}`", parse_mode="md")


@Client.on_message(Filters.command("setchatname", COMMAND_HAND_LER) & sudo_filter)
async def setchatname(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    if message.reply_to_message:
        chat_title = message.reply_to_message.text
    else:
        args = message.input_str.split(maxsplit=1)
        if len(args) >= 2:
            chat_title = args[0:]
    try:
        await client.set_chat_title(chat_id, chat_title)
    except Exception as ef:
        await client.reply_text(f"**Could not Change Chat Title due to:**\n`{ef}`", parse_mode="md")


@Client.on_message(Filters.command("setchatdesc", COMMAND_HAND_LER) & sudo_filter)
async def setchatdesc(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    if message.reply_to_message:
        chat_desc = message.reply_to_message.text
    else:
        args = message.input_str.split(maxsplit=1)
        if len(args) >= 2:
            chat_desc = args[0:]
    try:
        await client.set_chat_description(chat_id, chat_desc)
    except Exception as ef:
        await client.reply_text(f"**Could not Change Chat Title due to:**\n`{ef}`", parse_mode="md")
