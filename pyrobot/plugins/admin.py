import os
import asyncio
from pyrogram import Client, Filters, ChatPermissions
from pyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN, PRIVATE_GROUP_ID
from pyrobot.utils.admin_check import admin_check
from pyrobot.utils.pyrohelpers import extract_user
from pyrobot.utils.string import extract_time

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

`{COMMAND_HAND_LER}unrestrict` / unban / unmute: Unrestricts a user in the Group.
Usage: {COMMAND_HAND_LER}unmute (Username/User ID or reply to message)

`{COMMAND_HAND_LER}pin`: Pins the message in the Group.
Usage: {COMMAND_HAND_LER}pin (as a reply to the message)

`{COMMAND_HAND_LER}unpin`: unins the message in the Group.
Usage: {COMMAND_HAND_LER}unpin

`{COMMAND_HAND_LER}invite`: Add the user to your Group.
Usage: {COMMAND_HAND_LER}invite (Username or User ID)
"""


@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & Filters.me)
async def promote_usr(client, message):
    msg = await message.edit("`Trying to Promote user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.promote_member(user_id=user_id,
                                        can_change_info=False,
                                        can_delete_messages=True,
                                        can_restrict_members=True,
                                        can_invite_users=True,
                                        can_pin_messages=True)
        await asyncio.sleep(2)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Promoted** {user_first_name}")
            await client.send_message(PRIVATE_GROUP_ID, f"#PROMOTE\nPromoted {user_first_name} in chat {message.chat.title} (`{message.chat.id}`)")
        else:
            await message.edit(f"**Promoted** <a herf='tg://user?id={user_id}'>{user_first_name}</a>")
            await client.send_message(PRIVATE_GROUP_ID, f"#PROMOTE\nPromoted <a herf='tg://user?id={user_id}'>{user_first_name}</a> in chat {message.chat.title} (`{message.chat.id}`)")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("demote", COMMAND_HAND_LER) & Filters.me)
async def demote_usr(client, message):
    msg = await message.edit("`Trying to Demote user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.promote_member(user_id=user_id,
                                        can_change_info=False,
                                        can_delete_messages=False,
                                        can_restrict_members=False,
                                        can_invite_users=False,
                                        can_pin_messages=False)
        await asyncio.sleep(2)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Banned** {user_first_name}")
            await client.send_message(PRIVATE_GROUP_ID, f"#DEMOTE\nDemoted {user_first_name} in chat {message.chat.title} (`{message.chat.id}`)")
        else:
            await message.edit(f"**Banned** <a herf='tg://user?id={user_id}'>{user_first_name}</a>")
            await client.send_message(PRIVATE_GROUP_ID, f"#DEMOTE\nDemoted <a herf='tg://user?id={user_id}'>{user_first_name}</a> in chat {message.chat.title} (`{message.chat.id}`)")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("ban", COMMAND_HAND_LER) & Filters.me)
async def ban_usr(client, message):
    await message.edit("`Trying to Ban user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.kick_member(user_id=user_id)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Banned** {user_first_name}")
            await client.send_message(PRIVATE_GROUP_ID, f"#BAN\nBanned {user_first_name} in chat {message.chat.title} (`{message.chat.id}`)")
        else:
            await message.edit(f"**Banned** <a herf='tg://user?id={user_id}'>{user_first_name}</a>")
            await client.send_message(PRIVATE_GROUP_ID, f"#BAN\nBanned <a herf='tg://user?id={user_id}'>{user_first_name}</a> in chat {message.chat.title} (`{message.chat.id}`)")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("mute", COMMAND_HAND_LER) & Filters.me)
async def restrict_usr(client, message):
    await message.edit("`Trying to Mute user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.restrict_member(user_id=user_id,
            permisssions=ChatPermissions())
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Muted** {user_first_name}")
            await client.send_message(PRIVATE_GROUP_ID, f"#MUTE\nMuted {user_first_name} in chat {message.chat.title} (`{message.chat.id}`)")
        else:
            await message.edit(f"**Muted** <a herf='tg://user?id={user_id}'>{user_first_name}</a>")
            await client.send_message(PRIVATE_GROUP_ID, f"#MUTE\nMuted <a herf='tg://user?id={user_id}'>{user_first_name}</a> in chat {message.chat.title} (`{message.chat.id}`)")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("tmute", COMMAND_HAND_LER) & Filters.me)
async def restrict_usr(client, message):
    await message.edit("`Trying to Temporarily Mute user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = extract_user(message)
    until_date_val = extract_time(message.command[1])
    try:
        await message.chat.restrict_member(user_id=user_id,
            permisssions=ChatPermissions(),
            until_date=until_date_val)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**T Muted** {user_first_name} till {until_date_val}")
            await client.send_message(PRIVATE_GROUP_ID, f"#TEMPMUTE\nTemp. Muted {user_first_name} in chat {message.chat.title} (`{message.chat.id}`) till {until_date_val}")
        else:
            await message.edit(f"**T Muted** <a herf='tg://user?id={user_id}'>{user_first_name}</a>")
            await client.send_message(PRIVATE_GROUP_ID, f"#TEMPMUTE\nTemp. Muted <a herf='tg://user?id={user_id}'>{user_first_name}</a> in chat {message.chat.title} (`{message.chat.id}`) till {until_date_val}")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command(["unban", "unmute"], COMMAND_HAND_LER) & Filters.me)
async def unrestrict_usr(client, message):
    await message.edit("`Trying to Unrestrict user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.unban_member(user_id)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**UnRestricted** {user_first_name}")
            await client.send_message(PRIVATE_GROUP_ID, f"#UNRESTRICT\nUnrestricted {user_first_name} in chat {message.chat.title} (`{message.chat.id}`)")
        else:
            await message.edit(f"**UnRestricted** <a herf='tg://user?id={user_id}'>{user_first_name}</a>")
            await client.send_message(PRIVATE_GROUP_ID, f"#UNRESTRICT\nUnrestricted <a herf='tg://user?id={user_id}'>{user_first_name}</a> in chat {message.chat.title} (`{message.chat.id}`) till {until_date_val}")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("pin", COMMAND_HAND_LER) & Filters.me)
async def pin_message(client, message):
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


@Client.on_message(Filters.command("invite", COMMAND_HAND_LER) & Filters.me)
async def invite_user(client, message):
    if len(message.command) > 2:
        await message.edit(f"__Only one user can be invited at a time,\ncheck__ `{COMMAND_HAND_LER}help` __for more info.__")
        return
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.add_members(user_id=user_id)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Added** {user_first_name}")
            await client.send_message(PRIVATE_GROUP_ID, f"#INVITE\Added {user_first_name} in chat {message.chat.title} (`{message.chat.id}`)")
        else:
            await message.edit(f"**Added** <a herf='tg://user?id={user_id}'>{user_first_name}</a>")
            await client.send_message(PRIVATE_GROUP_ID, f"#INVITE\Added <a herf='tg://user?id={user_id}'>{user_first_name}</a> in chat {message.chat.title} (`{message.chat.id}`) till {until_date_val}")
    except Exception as ef:
        await message.edit(f"<b>Error:</b>\n`{ef}`")
        return
