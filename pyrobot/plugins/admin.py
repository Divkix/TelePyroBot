import asyncio
from pyrogram import Client, Filters, ChatPermissions
from pyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN

from pyrobot.utils.extract_user import extract_user
from pyrobot.utils.admin_check import admin_check
from pyrobot.utils.list_to_string import listToString


@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & Filters.me)
async def promote_usr(client, message):
    try:
        rm = await message.edit("`Trying to Promote User.. Hang on!! ⏳`", parse_mode="md")
    except:
        rm = await message.reply_text("`Trying to Promote User.. Hang on!! ⏳`", parse_mode="md")
    is_admin = await admin_check(message)

    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)
    chat_id = message.chat.id
    if user_id and chat_id:
        try:
            await client.promote_chat_member(chat_id, user_id,
                                            can_change_info=False,
                                            can_delete_messages=True,
                                            can_restrict_members=True,
                                            can_invite_users=True,
                                            can_pin_messages=True)
            await asyncio.sleep(2)
            await rm.edit(f"`👑 Promoted` [{user_first_name}](tg://user?id={user_id}) `Successfully...`", parse_mode="md")
        except Exception as ef:
            await rm.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("demote", COMMAND_HAND_LER) & Filters.me)
async def demote_usr(client, message):
    try:
        rm = await message.edit("`Trying to Demote User.. Hang on!! ⏳`", parse_mode="md")
    except:
        rm = await message.reply_text("`Trying to Demote User.. Hang on!! ⏳`", parse_mode="md")
    is_admin = await admin_check(message)

    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)
    chat_id = message.chat.id

    if user_id and chat_id:
        try:
            await client.promote_chat_member(chat_id, user_id,
                                            can_change_info=False,
                                            can_delete_messages=False,
                                            can_restrict_members=False,
                                            can_invite_users=False,
                                            can_pin_messages=False)
            await asyncio.sleep(2)
            await rm.edit(f"`Demoted` [{user_first_name}](tg://user?id={user_id}) `Successfully...`", parse_mode="md")
        except Exception as ef:
            await rm.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("ban", COMMAND_HAND_LER) & Filters.me)
async def ban_usr(client, message):
    try:
        rm = await message.edit("`Trying to Ban User.. Hang on!! ⏳`", parse_mode="md")
    except:
        rm = await message.reply_text("`Trying to Ban User.. Hang on!! ⏳`", parse_mode="md")
    is_admin = await admin_check(message)

    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.kick_member(user_id=user_id)
        await rm.edit(f"`Banned` [{user_first_name}](tg://user?id={user_id}) `Successfully...`", parse_mode="md")
    except Exception as ef:
        await rm.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("mute", COMMAND_HAND_LER) & Filters.me)
async def ban_usr(client, message):
    try:
        rm = await message.edit("`Trying to Mute User.. Hang on!! ⏳`", parse_mode="md")
    except:
        rm = await message.reply_text("`Trying to Mute User.. Hang on!! ⏳`", parse_mode="md")
    is_admin = await admin_check(message)

    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions())
        await rm.edit(f"`Muted` [{user_first_name}](tg://user?id={user_id}) `Successfully...`", parse_mode="md")
    except Exception as ef:
        await rm.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command(["unmute", "unban"], COMMAND_HAND_LER) & Filters.me)
async def ban_usr(client, message):
    try:
        rm = await message.edit("`Trying to Unrestrict User.. Hang on!! ⏳`", parse_mode="md")
    except:
        rm = await message.reply_text("`Trying to Unrestrict User.. Hang on!! ⏳`", parse_mode="md")
    is_admin = await admin_check(message)

    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id)
        await rm.edit(f"`Unrestrict` [{user_first_name}](tg://user?id={user_id}) `Successfully...`", parse_mode="md")
    except Exception as ef:
        await rm.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("pin", COMMAND_HAND_LER) & Filters.me)
async def pin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        try:
            rm = await message.edit("`Trying to pin message...`")
        except:
            rm = await message.reply_text("`Trying to pin message...`")
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
                disable_notification=disable_notification)
            await rm.edit("`Pinned message!`", parse_mode="md")
        else:
            await rm.edit("`Reply to a message to which you want to pin...`", parse_mode="md")


@Client.on_message(Filters.command("unpin", COMMAND_HAND_LER) & Filters.me)
async def unpin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        try:
            rm = await message.edit("`Trying to unpin message...`")
        except:
            rm = await message.reply_text("`Trying to unpin message...`")
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.unpin_chat_message(chat_id)
        await rm.edit("`Unpinned message!`", parse_mode="md")


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
    link = client.export_chat_invite_link(chat_id)
    await message.reply_text(f"**Link for Chat:**\n`{link}`", parse_mode="md")


@Client.on_message(Filters.command("setchatpic", COMMAND_HAND_LER) & Filters.me)
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


@Client.on_message(Filters.command("delchatpic", COMMAND_HAND_LER) & Filters.me)
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


@Client.on_message(Filters.command("setchatname", COMMAND_HAND_LER) & Filters.me)
async def setchatname(client, message):
    try:
        rm = await message.edit("__Trying to Change Chat Name!__")
    except:
        rm = await message.reply_text("__Trying to Change Chat Name!__")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    if message.reply_to_message:
        chat_title = message.reply_to_message.text
    else:
        chat_title = listToString(message.command[1:])
    try:
        await client.set_chat_title(chat_id, chat_title)
        await rm.edit(f"<b>Changed Chat Name to:</b> <code>{chat_title}</code>")
    except Exception as ef:
        await rm.edit(f"**Could not Change Chat Title due to:**\n`{ef}`", parse_mode="md")


@Client.on_message(Filters.command("setchatdesc", COMMAND_HAND_LER) & Filters.me)
async def setchatdesc(client, message):
    try:
        rm = await message.edit("__Trying to Change Chat Desciption!__")
    except:
        rm = await message.reply_text("__Trying to Change Chat Desciption!__")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    if message.reply_to_message:
        chat_desc = message.reply_to_message.text
    else:
        chat_desc = listToString(message.command[1:])
    try:
        await client.set_chat_description(chat_id, chat_desc)
        await rm.edit(f"<b>Changed Chat Name to:</b> <code>{chat_title}</code>")
    except Exception as ef:
        await rm.edit(f"**Could not Change Chat Desciption due to:**\n`{ef}`", parse_mode="md")


@Client.on_message(Filters.command("purge", COMMAND_HAND_LER) & Filters.me)
async def purge(client, message):
    """ purge upto the replied message """
    if message.chat.type not in (("supergroup", "channel")):
        return

    is_admin = await admin_check(message)

    if not is_admin:
        return

    status_message = await message.reply_text("Purging messages...", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(message.reply_to_message.message_id, message.message_id):
            message_ids.append(a_s_message_id)
            if len(message_ids) == TG_MAX_SELECT_LEN:
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True)
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True)
            count_del_etion_s += len(message_ids)

    await status_message.edit_text(
        f"Deleted `{count_del_etion_s}` messages", parse_mode="md")
    await asyncio.sleep(5)
    await status_message.delete()
