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
    chat_id = message.chat.id
    if not is_admin:
        await msg.edit("`I'm not admin, bot plays Hat Bhen ki Lodi on Spotify!`")
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            from_user = await client.get_users(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    try:
        get_mem = await client.get_chat_member(chat_id, from_user)
        await client.promote_chat_member(chat_id, from_user,
                                        can_change_info=False,
                                        can_delete_messages=True,
                                        can_restrict_members=True,
                                        can_invite_users=True,
                                        can_pin_messages=True)
        await asyncio.sleep(2)
        await message.edit(f"`👑 Promoted {get_mem.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("demote", COMMAND_HAND_LER) & Filters.me)
async def demote_usr(client, message):
    msg = await message.edit("`Trying to Demote user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        await msg.edit("`I'm not admin, bot plays Hat Bhen ki Lodi on Spotify!`")
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            from_user = await client.get_users(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    try:
        get_mem = await client.get_chat_member(chat_id, from_user)
        await client.promote_chat_member(chat_id, from_user,
                                        can_change_info=False,
                                        can_delete_messages=False,
                                        can_restrict_members=False,
                                        can_invite_users=False,
                                        can_pin_messages=False)
        await asyncio.sleep(2)
        await message.edit(f"`Demoted {get_mem.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("ban", COMMAND_HAND_LER) & Filters.me)
async def ban_usr(client, message):
    await message.edit("`Trying to Ban user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    if len(message.command) == 2:
        user_id = message.text.split(" ")[1]
        try:
            from_user = await client.get_users(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    try:
        get_mem = await client.get_chat_member(message.chat.id, from_user)
        await client.kick_chat_member(message.chat.id, user_id)
        await message.edit(f"`Banned {get_mem.first_name} `")
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
            from_user = await client.get_users(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    try:
        get_mem = await client.get_chat_member(chat_id, from_user)
        await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        await message.edit(f"`Muted {get_mem.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("unban", COMMAND_HAND_LER) & Filters.me)
async def unrestrict_usr(client, message):
    await message.edit("`Trying to Unban user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            from_user = await client.get_users(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    try:
        get_mem = await client.get_chat_member(chat_id, from_user)
        await client.unban_chat_member(chat_id, from_user)
        await message.edit(f"`Unbanned {get_mem.first_name} `")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("unmute", COMMAND_HAND_LER) & Filters.me)
async def unrestrict_usr(client, message):
    await message.edit("`Trying to Unmute user...`")
    is_admin = await admin_check(message)
    get_group = await client.get_chat(chat_id)
    chat_id = message.chat.id
    amsg = get_group.permissions.can_send_messages
    amedia = get_group.permissions.can_send_media_messages
    astickers = get_group.permissions.can_send_stickers
    aanimations = get_group.permissions.can_send_animations
    agames = get_group.permissions.can_send_games
    ainlinebots = get_group.permissions.can_use_inline_bots
    awebprev = get_group.permissions.can_add_web_page_previews
    apolls = get_group.permissions.can_send_polls
    ainfo = get_group.permissions.can_change_info
    ainvite = get_group.permissions.can_invite_users
    apin = get_group.permissions.can_pin_messages
    if not is_admin:
        return
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            from_user = await client.get_users(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    try:
        get_mem = await client.get_chat_member(chat_id, from_user)
        await client.restrict_chat_member(chat_id, user_id,
                                            ChatPermissions(
                                            can_send_messages=amsg,
                                            can_send_media_messages=amedia,
                                            can_send_stickers=astickers,
                                            can_send_animations=aanimations,
                                            can_send_games=agames,
                                            can_use_inline_bots=ainlinebots,
                                            can_add_web_page_previews=awebprev,
                                            can_send_polls=apolls,
                                            can_change_info=ainfo,
                                            can_invite_users=ainvite,
                                            can_pin_messages=apin))
        await message.edit(f"`Unmuted {get_mem.first_name} `")
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


@Client.on_message(Filters.command("invite", COMMAND_HAND_LER) & Filters.me)
async def invite_user(client, message):
    if len(message.command) > 2:
        await message.edit("__Only one user can be invited at a time,\ncheck__ `{COMMAND_HAND_LER}help` __for more info.__")
        return
    user_id = message.text.split(' ', 1)[1]
    chat_id = message.chat.id
    if user_id:
        try:
            from_user = await client.get_users(user_id)
        except:
            await message.edit("No User found!")
            return
    else:
        await message.edit("User_id not defined")
        return
    try:
        await client.add_chat_members(chat_id, from_user.id)
    except Exception as ef:
        await message.edit(f"<b>Error:</b>\n`{ef}`")
        return
