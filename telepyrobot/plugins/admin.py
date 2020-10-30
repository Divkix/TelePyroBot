import os
import asyncio
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
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


@TelePyroBot.on_message(filters.command("promote", COMMAND_HAND_LER) & filters.me)
async def promote_usr(c: TelePyroBot, m: Message):
    await m.edit("`Trying to Promote user...`")
    is_admin = await admin_check(c, m)
    if not is_admin:
        return
        return
    user_id, user_first_name = await extract_user(c, m)
    try:
        await m.chat.promote_member(
            user_id=user_id,
            can_change_info=False,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True,
        )
        await asyncio.sleep(2)
        if str(user_id).lower().startswith("@"):
            await m.edit(f"**Promoted** {user_first_name}")
            await c.send_message(
                PRIVATE_GROUP_ID,
                f"#PROMOTE\nPromoted {user_first_name} in chat {m.chat.title}",
            )
        else:
            await m.edit(
                f"**Promoted** {mention_markdown(user_first_name, user_id)}"
            )
            await c.send_message(
                PRIVATE_GROUP_ID,
                "#PROMOTE\nPromoted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), m.chat.title
                ),
            )
    except Exception as ef:
        await m.edit(f"**Error:**\n\n`{ef}`")
    return


@TelePyroBot.on_message(filters.command("demote", COMMAND_HAND_LER) & filters.me)
async def demote_usr(c: TelePyroBot, m: Message):
    await m.edit("`Trying to Demote user...`")
    is_admin = await admin_check(c, m)
    if not is_admin:
        return
        return
    user_id, user_first_name = await extract_user(c, m)
    try:
        await m.chat.promote_member(
            user_id=user_id,
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
        )
        await asyncio.sleep(2)
        if str(user_id).lower().startswith("@"):
            await m.edit(f"**Demoted** {user_first_name}")
            await c.send_message(
                PRIVATE_GROUP_ID,
                f"#DEMOTE\nDemoted {user_first_name} in chat {m.chat.title}",
            )
        else:
            await m.edit(
                f"**Demoted** {mention_markdown(user_first_name, user_id)}"
            )
            await c.send_message(
                PRIVATE_GROUP_ID,
                "#DEMOTE\nDemoted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), m.chat.title
                ),
            )
    except Exception as ef:
        await m.edit(f"**Error:**\n\n`{ef}`")


@TelePyroBot.on_message(filters.command("ban", COMMAND_HAND_LER) & filters.me)
async def ban_usr(c: TelePyroBot, m: Message):
    await m.edit("`Trying to Ban user...`")
    is_admin = await admin_check(c, m)
    if not is_admin:
        return
    user_id, user_first_name = await extract_user(c, m)
    if m.reply_to_message:
        await c.delete_messages(m.chat.id, m.reply_to_message.message_id)
    try:
        await m.chat.kick_member(user_id=user_id)
        if str(user_id).lower().startswith("@"):
            await m.edit(f"**Banned** {user_first_name}")
            await c.send_message(
                PRIVATE_GROUP_ID,
                f"#BAN\nBanned {user_first_name} in chat {m.chat.title}",
            )
        else:
            await m.edit(
                f"**Banned** {mention_markdown(user_first_name, user_id)}"
            )
            await c.send_message(
                PRIVATE_GROUP_ID,
                "#BAN\nBanned {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), m.chat.title
                ),
            )
    except Exception as ef:
        await m.edit(f"**Error:**\n\n`{ef}`")


@TelePyroBot.on_message(filters.command("mute", COMMAND_HAND_LER) & filters.me)
async def restrict_usr(c: TelePyroBot, m: Message):
    await m.edit("`Trying to Mute user...`")
    is_admin = await admin_check(c, m)
    chat_id = m.chat.id
    if not is_admin:
        await m.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await m.delete()
        return
    user_id, user_first_name = await extract_user(c, m)
    try:
        await m.chat.restrict_member(user_id=user_id, permisssions=ChatPermissions())
        if str(user_id).lower().startswith("@"):
            await m.edit(f"**Muted** {user_first_name}")
            await c.send_message(
                PRIVATE_GROUP_ID,
                f"#MUTE\nMuted {user_first_name} in chat {m.chat.title}",
            )
        else:
            await m.edit(
                f"**Muted** {mention_markdown(user_first_name, user_id)}"
            )
            await c.send_message(
                PRIVATE_GROUP_ID,
                "#MUTE\nMuted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), m.chat.title
                ),
            )
    except Exception as ef:
        await m.edit(f"**Error:**\n\n`{ef}`")


@TelePyroBot.on_message(
    filters.command(["unban", "unmute"], COMMAND_HAND_LER) & filters.me
)
async def unrestrict_usr(c: TelePyroBot, m: Message):
    await m.edit("`Trying to Unrestrict user...`")
    is_admin = await admin_check(c, m)
    if not is_admin:
        return
        return
    user_id, user_first_name = await extract_user(c, m)
    try:
        await m.chat.unban_member(user_id)
        if str(user_id).lower().startswith("@"):
            await m.edit(f"**UnRestricted** {user_first_name}")
            await c.send_message(
                PRIVATE_GROUP_ID,
                f"#UNRESTRICT\nUnrestricted {user_first_name} in chat {m.chat.title}",
            )
        else:
            await m.edit(
                f"**UnRestricted** {mention_markdown(user_first_name, user_id)}"
            )
            await c.send_message(
                PRIVATE_GROUP_ID,
                "#UNRESTRICT\nUnrestricted {} in chat {}".format(
                    mention_markdown(user_first_name, user_id), m.chat.title
                ),
            )
    except Exception as ef:
        await m.edit(f"**Error:**\n\n`{ef}`")
