import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from telepyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN, PRIVATE_GROUP_ID
from telepyrobot.utils.admin_check import admin_check
from telepyrobot.utils.pyrohelpers import extract_user
from telepyrobot.utils.parser import mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Manage Tasks with your userbot easily, great plugin for people to manage their chats.

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
"""


@Client.on_message(filters.command("promote", COMMAND_HAND_LER) & filters.me)
async def promote_usr(client, message):
    msg = await message.edit("`Trying to Promote user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = await extract_user(client, message)
    try:
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=False,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True,
        )
        await asyncio.sleep(2)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Promoted** {user_first_name}")
            await client.send_message(
                PRIVATE_GROUP_ID,
                f"#PROMOTE\nPromoted {user_first_name} in chat {message.chat.title}",
            )
        else:
            await message.edit(
                "**Promoted** {}".format(mention_markdown(user_first_name, user_id))
            )
            await client.send_message(
                PRIVATE_GROUP_ID,
                "#PROMOTE\nPromoted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), message.chat.title
                ),
            )
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(filters.command("demote", COMMAND_HAND_LER) & filters.me)
async def demote_usr(client, message):
    msg = await message.edit("`Trying to Demote user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = await extract_user(client, message)
    try:
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
        )
        await asyncio.sleep(2)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Demoted** {user_first_name}")
            await client.send_message(
                PRIVATE_GROUP_ID,
                f"#DEMOTE\nDemoted {user_first_name} in chat {message.chat.title}",
            )
        else:
            await message.edit(
                "**Demoted** {}".format(mention_markdown(user_first_name, user_id))
            )
            await client.send_message(
                PRIVATE_GROUP_ID,
                "#DEMOTE\nDemoted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), message.chat.title
                ),
            )
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(filters.command("ban", COMMAND_HAND_LER) & filters.me)
async def ban_usr(client, message):
    await message.edit("`Trying to Ban user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = await extract_user(client, message)
    if message.reply_to_message:
        await client.delete_messages(
            message.chat.id, message.reply_to_message.message_id
        )
    try:
        await message.chat.kick_member(user_id=user_id)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Banned** {user_first_name}")
            await client.send_message(
                PRIVATE_GROUP_ID,
                f"#BAN\nBanned {user_first_name} in chat {message.chat.title}",
            )
        else:
            await message.edit(
                "**Banned** {}".format(mention_markdown(user_first_name, user_id))
            )
            await client.send_message(
                PRIVATE_GROUP_ID,
                "#BAN\nBanned {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), message.chat.title
                ),
            )
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(filters.command("mute", COMMAND_HAND_LER) & filters.me)
async def restrict_usr(client, message):
    await message.edit("`Trying to Mute user...`")
    is_admin = await admin_check(message)
    chat_id = message.chat.id
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = await extract_user(client, message)
    try:
        await message.chat.restrict_member(
            user_id=user_id, permisssions=ChatPermissions()
        )
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Muted** {user_first_name}")
            await client.send_message(
                PRIVATE_GROUP_ID,
                f"#MUTE\nMuted {user_first_name} in chat {message.chat.title}",
            )
        else:
            await message.edit(
                "**Muted** {}".format(mention_markdown(user_first_name, user_id))
            )
            await client.send_message(
                PRIVATE_GROUP_ID,
                "#MUTE\nMuted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), message.chat.title
                ),
            )
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(filters.command(["unban", "unmute"], COMMAND_HAND_LER) & filters.me)
async def unrestrict_usr(client, message):
    await message.edit("`Trying to Unrestrict user...`")
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    user_id, user_first_name = await extract_user(client, message)
    try:
        await message.chat.unban_member(user_id)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**UnRestricted** {user_first_name}")
            await client.send_message(
                PRIVATE_GROUP_ID,
                f"#UNRESTRICT\nUnrestricted {user_first_name} in chat {message.chat.title}",
            )
        else:
            await message.edit(
                "**UnRestricted** {}".format(mention_markdown(user_first_name, user_id))
            )
            await client.send_message(
                PRIVATE_GROUP_ID,
                "#UNRESTRICT\nUnrestricted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), message.chat.title
                ),
            )
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")
