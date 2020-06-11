import os
import asyncio
from pyrogram import Client, Filters, ChatPermissions
from pyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN
from pyrobot.utils.admin_check import admin_check

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}promote`: Promotes a user in the Group.
Usage: {COMMAND_HAND_LER}promote (Username/User ID or reply to message)

`{COMMAND_HAND_LER}demote`: Demotes a user in the Group.
Usage: {COMMAND_HAND_LER}demote (Username/User ID or reply to message)

`{COMMAND_HAND_LER}ban`: Bans a user in the Group.
Usage: {COMMAND_HAND_LER}ban (Username/User ID or reply to message)

`{COMMAND_HAND_LER}mute`: Mutes a user in the Group.
Usage: {COMMAND_HAND_LER}mute (Username/User ID or reply to message)

`{COMMAND_HAND_LER}unrestrict` \ unban \ unmute: Unrestricts a user in the Group.
Usage: {COMMAND_HAND_LER}unmute (Username/User ID or reply to message)

`{COMMAND_HAND_LER}pin`: Pins the message in the Group.
Usage: {COMMAND_HAND_LER}pin (as a reply to the message)

`{COMMAND_HAND_LER}unpin`: Pins the message in the Group.
Usage: {COMMAND_HAND_LER}unpin

`{COMMAND_HAND_LER}purge`: Deletes messages upto replied message.
Usage: {COMMAND_HAND_LER}purge (as a reply to the message)

`{COMMAND_HAND_LER}del`: Deletes a single message.
Usage: {COMMAND_HAND_LER}del (as a reply to the message)

`{COMMAND_HAND_LER}invite`: Add the user to your Group.
Usage: {COMMAND_HAND_LER}invite (Username or User ID)
"""


@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & Filters.me)
async def promote_usr(client, message):
    await message.edit("`Trying to Promote user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            user_id = await client.get_users(user_id)
            user_chat = await client.get_chat(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        user_id = await client.get_users(message.reply_to_message.from_user.id)
        user_chat = await client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    try:
        await client.promote_chat_member(chat_id, user_id,
                                        can_change_info=False,
                                        can_delete_messages=True,
                                        can_restrict_members=True,
                                        can_invite_users=True,
                                        can_pin_messages=True)
        await asyncio.sleep(2)
        await message.edit(f"`👑 Promoted {user_id.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("demote", COMMAND_HAND_LER) & Filters.me)
async def demote_usr(client, message):
    await message.edit("`Trying to Demote user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            user_id = await client.get_users(user_id)
            user_chat = await client.get_chat(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        user_id = await client.get_users(message.reply_to_message.from_user.id)
        user_chat = await client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    try:
        await client.promote_chat_member(chat_id, user_id,
                                        can_change_info=False,
                                        can_delete_messages=False,
                                        can_restrict_members=False,
                                        can_invite_users=False,
                                        can_pin_messages=False)
        await asyncio.sleep(2)
        await message.edit(f"`Demoted {user_id.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("ban", COMMAND_HAND_LER) & Filters.me)
async def ban_usr(client, message):
    await message.edit("`Trying to Ban user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            user_id = await client.get_users(user_id)
            user_chat = await client.get_chat(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        user_id = await client.get_users(message.reply_to_message.from_user.id)
        user_chat = await client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.kick_member(user_id)
        await message.edit(f"`Banned {user_id.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("mute", COMMAND_HAND_LER) & Filters.me)
async def restrict_usr(client, message):
    await message.edit("`Trying to Mute user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            user_id = await client.get_users(user_id)
            user_chat = await client.get_chat(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        user_id = await client.get_users(message.reply_to_message.from_user.id)
        user_chat = await client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions())
        await message.edit(f"`Muted {user_id.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command(["unmute", "unban", "unrestrict"], COMMAND_HAND_LER) & Filters.me)
async def unrestrict_usr(client, message):
    await message.edit("`Trying to Unrestrict user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            user_id = await client.get_users(user_id)
            user_chat = await client.get_chat(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        user_id = await client.get_users(message.reply_to_message.from_user.id)
        user_chat = await client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.unban_member(
            user_id=user_id)
        await message.edit(f"`Unrestricted {user_id.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("pin", COMMAND_HAND_LER) & Filters.me)
async def pin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        await message.edit("`Trying to pin message...`")
        is_admin = await admin_check(message)
        if not is_admin:
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


@Client.on_message(Filters.command("unpin", COMMAND_HAND_LER) & Filters.me)
async def unpin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        await message.edit("`Trying to unpin message...`")
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.unpin_chat_message(chat_id)
        await message.edit("`Unpinned message!`")
        await asyncio.sleep(3)
        await message.delete()


@Client.on_message(Filters.command("purge", COMMAND_HAND_LER) & Filters.me)
async def purge(client, message):
    if message.chat.type == "supergroup":
        is_admin = await admin_check(message)
        if not is_admin:
            return

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

    await message.edit(f"`Deleted <u>{count_del_etion_s}</u> messages`")
    await asyncio.sleep(3)
    await message.delete()


@Client.on_message(Filters.command("del", COMMAND_HAND_LER) & Filters.me)
async def del_msg(client, message):
    await message.edit("`Trying to delete message`")
    if message.chat.type == "supergroup":
        is_admin = await admin_check(message)
        if not is_admin:
            return
    chat_id = message.chat.id
    message_ids = []
    if message.reply_to_message:
        try:
            message_ids.append(message.reply_to_message.message_id)
            await client.delete_messages(chat_id=chat_id,
                            message_ids=message_ids,
                            revoke=True)
        except Exception as ef:
            await message.edit(f"<b>Error</b>:\n`{ef}`")
        await message.delete()
    else:
        await message.edit("`Reply to a message to delete it!`")
        return


@Client.on_message(Filters.command("invite", COMMAND_HAND_LER) & Filters.me)
async def invite_user(client, message):
    if len(message.command) > 2:
        await message.edit("__Only one user can be invited at a time,\ncheck__ `{COMMAND_HAND_LER}help` __for more info.__")
        return
    user_id = message.text.split(' ', 1)[1]
    if user_id:
        try:
            from_user = await client.get_users(user_id)
            from_chat = await client.get_chat(user_id)
        except Exception:
            await message.edit("no valid user_id or message specified")
            return
    else:
        await message.edit("no valid user_id or message specified")
        return
    try:
        await client.add_chat_members(message.chat.id, user_id)
    except Exception as ef:
        await message.edit(f"<b>Error:</b>\n`{ef}`")
        return
