import os
import time
import asyncio
from datetime import datetime
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from telepyrobot import (
    COMMAND_HAND_LER,
    TG_MAX_SELECT_LEN,
    PRIVATE_GROUP_ID,
    OWNER_ID,
    OWNER_NAME,
)
from telepyrobot.utils.admin_check import admin_check
from telepyrobot.utils.parser import mention_markdown, escape_markdown


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__HELP__ = f"""
Use this to lock group permissions.
Allows you to lock some common permission types in the chat.

**Types:** all, msg, media, polls, invite, pin, info,
        webprev, inlinebots, animations, games, stickers

**Usage:**
`{COMMAND_HAND_LER}lock <type>`: Lock Chat permission
`{COMMAND_HAND_LER}unlock <type>`: Unlock Chat permission
`{COMMAND_HAND_LER}vperm`: View Chat permission

**NOTE:** Requires proper admin rights in the chat!!
"""


@TelePyroBot.on_message(filters.command("lock", COMMAND_HAND_LER) & filters.me)
async def lock_perm(c: Client, m: Message):
    msg = ""
    media = ""
    stickers = ""
    animations = ""
    games = ""
    inlinebots = ""
    webprev = ""
    polls = ""
    info = ""
    invite = ""
    pin = ""
    perm = ""

    lock_type = message.text.split(" ", 1)[1]
    chat_id = message.chat.id

    if not lock_type:
        await m.edit("`I Can't Lock Nothing! (－‸ლ)`")
        await asyncio.sleep(5)
        await m.delete()
        return

    get_perm = await client.get_chat(chat_id)

    msg = get_perm.permissions.can_send_messages
    media = get_perm.permissions.can_send_media_messages
    stickers = get_perm.permissions.can_send_stickers
    animations = get_perm.permissions.can_send_animations
    games = get_perm.permissions.can_send_games
    inlinebots = get_perm.permissions.can_use_inline_bots
    webprev = get_perm.permissions.can_add_web_page_previews
    polls = get_perm.permissions.can_send_polls
    info = get_perm.permissions.can_change_info
    invite = get_perm.permissions.can_invite_users
    pin = get_perm.permissions.can_pin_messages

    if lock_type == "all":
        try:
            await client.set_chat_permissions(chat_id, ChatPermissions())
            await m.edit(text="**🔒 Locked all permission from this Chat!**")
            await asyncio.sleep(5)
            await m.delete()
            await c.send_message(
                PRIVATE_GROUP_ID,
                "#LOCK\n\nCHAT: `{}` (`{}`)\nPERMISSIONS: `All Permissions`".format(
                    get_perm.title, chat_id
                ),
            )

        except Exception as e_f:
            await m.edit(
                f"`I don't have permission to do that ＞︿＜`\n\n**ERROR:** `{e_f}`"
            )
            await asyncio.sleep(5)
            await m.delete()

        return

    if lock_type == "msg":
        msg = False
        perm = "messages"

    elif lock_type == "media":
        media = False
        perm = "audios, documents, photos, videos, video notes, voice notes"

    elif lock_type == "stickers":
        stickers = False
        perm = "stickers"

    elif lock_type == "animations":
        animations = False
        perm = "animations"

    elif lock_type == "games":
        games = False
        perm = "games"

    elif lock_type == "inlinebots":
        inlinebots = False
        perm = "inline bots"

    elif lock_type == "webprev":
        webprev = False
        perm = "web page previews"

    elif lock_type == "polls":
        polls = False
        perm = "polls"

    elif lock_type == "info":
        info = False
        perm = "info"

    elif lock_type == "invite":
        invite = False
        perm = "invite"

    elif lock_type == "pin":
        pin = False
        perm = "pin"

    else:
        await m.edit("`Invalid Lock Type! ¯\_(ツ)_/¯`")
        await asyncio.sleep(5)
        await m.delete()
        return

    try:
        await client.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=msg,
                can_send_media_messages=media,
                can_send_stickers=stickers,
                can_send_animations=animations,
                can_send_games=games,
                can_use_inline_bots=inlinebots,
                can_add_web_page_previews=webprev,
                can_send_polls=polls,
                can_change_info=info,
                can_invite_users=invite,
                can_pin_messages=pin,
            ),
        )

        await m.edit(text=f"**🔒 Locked {perm} for this chat!**")
        await asyncio.sleep(5)
        await m.delete()
        await c.send_message(
            PRIVATE_GROUP_ID,
            "#LOCK\n\nCHAT: `{}` (`{}`)\nPERMISSIONS: `{} Permission`".format(
                get_perm.title, chat_id, perm
            ),
        )

    except Exception as e_f:
        await m.edit(
            text=r"`i don't have permission to do that ＞︿＜`\n\n" f"**ERROR:** `{e_f}`"
        )
        await asyncio.sleep(5)
        await m.delete()
    return


@TelePyroBot.on_message(filters.command("unlock", COMMAND_HAND_LER) & filters.me)
async def unlock_perm(c: Client, m: Message):
    umsg = ""
    umedia = ""
    ustickers = ""
    uanimations = ""
    ugames = ""
    uinlinebots = ""
    uwebprev = ""
    upolls = ""
    uinfo = ""
    uinvite = ""
    upin = ""
    uperm = ""

    unlock_type = message.text.split(" ", 1)[1]
    chat_id = message.chat.id

    if not unlock_type:
        await m.edit(text=r"`I Can't Unlock Nothing! (－‸ლ)`")
        await asyncio.sleep(5)
        await m.delete()
        return

    get_uperm = await client.get_chat(chat_id)

    umsg = get_uperm.permissions.can_send_messages
    umedia = get_uperm.permissions.can_send_media_messages
    ustickers = get_uperm.permissions.can_send_stickers
    uanimations = get_uperm.permissions.can_send_animations
    ugames = get_uperm.permissions.can_send_games
    uinlinebots = get_uperm.permissions.can_use_inline_bots
    uwebprev = get_uperm.permissions.can_add_web_page_previews
    upolls = get_uperm.permissions.can_send_polls
    uinfo = get_uperm.permissions.can_change_info
    uinvite = get_uperm.permissions.can_invite_users
    upin = get_uperm.permissions.can_pin_messages

    if unlock_type == "all":
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_stickers=True,
                    can_send_animations=True,
                    can_send_games=True,
                    can_use_inline_bots=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_add_web_page_previews=True,
                ),
            )

            await m.edit("**🔓 Unlocked all permission from this Chat!**")
            await asyncio.sleep(5)
            await m.delete()
            await c.send_message(
                PRIVATE_GROUP_ID,
                "#UNLOCK\n\nCHAT: `{}` (`{}`)\nPERMISSIONS: `All Permissions`".format(
                    message.chat.title, message.chat.id
                ),
            )

        except Exception as e_f:
            await m.edit(
                f"`I don't have permission to do that ＞︿＜`\n\n**ERROR:** `{e_f}`"
            )
            await asyncio.sleep(5)
            await m.delete()
        return

    if unlock_type == "msg":
        umsg = True
        uperm = "messages"

    elif unlock_type == "media":
        umedia = True
        uperm = "audios, documents, photos, videos, video notes, voice notes"

    elif unlock_type == "stickers":
        ustickers = True
        uperm = "stickers"

    elif unlock_type == "animations":
        uanimations = True
        uperm = "animations"

    elif unlock_type == "games":
        ugames = True
        uperm = "games"

    elif unlock_type == "inlinebots":
        uinlinebots = True
        uperm = "inline bots"

    elif unlock_type == "webprev":
        uwebprev = True
        uperm = "web page previews"

    elif unlock_type == "polls":
        upolls = True
        uperm = "polls"

    elif unlock_type == "info":
        uinfo = True
        uperm = "info"

    elif unlock_type == "invite":
        uinvite = True
        uperm = "invite"

    elif unlock_type == "pin":
        upin = True
        uperm = "pin"

    else:
        await m.edit("`Invalid Unlock Type! ¯\_(ツ)_/¯`")
        await asyncio.sleep(5)
        await m.delete()
        return

    try:
        await client.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=umsg,
                can_send_media_messages=umedia,
                can_send_stickers=ustickers,
                can_send_animations=uanimations,
                can_send_games=ugames,
                can_use_inline_bots=uinlinebots,
                can_add_web_page_previews=uwebprev,
                can_send_polls=upolls,
                can_change_info=uinfo,
                can_invite_users=uinvite,
                can_pin_messages=upin,
            ),
        )

        await m.edit(f"**🔓 Unlocked {uperm} for this chat!**")
        await asyncio.sleep(5)
        await m.delete()
        await c.send_message(
            PRIVATE_GROUP_ID,
            "#UNLOCK\n\nCHAT: `{}` (`{}`)\nPERMISSION: `{} Permission`".format(
                message.chat.title, message.chat.id, uperm
            ),
        )

    except Exception as e_f:
        await m.edit(f"`I don't have permission to do that ＞︿＜`\n\n**ERROR:** `{e_f}`")
    return


@TelePyroBot.on_message(filters.command("vperm", COMMAND_HAND_LER) & filters.me)
async def view_perm(c: Client, m: Message):
    v_perm = ""
    vmsg = ""
    vmedia = ""
    vstickers = ""
    vanimations = ""
    vgames = ""
    vinlinebots = ""
    vwebprev = ""
    vpolls = ""
    vinfo = ""
    vinvite = ""
    vpin = ""

    await m.edit("`Checking group permissions... Hang on!! ⏳`")

    v_perm = await client.get_chat(message.chat.id)

    def convert_to_emoji(val: bool):
        if val is True:
            return "✅"
        return "❌"

    vmsg = convert_to_emoji(v_perm.permissions.can_send_messages)
    vmedia = convert_to_emoji(v_perm.permissions.can_send_media_messages)
    vstickers = convert_to_emoji(v_perm.permissions.can_send_stickers)
    vanimations = convert_to_emoji(v_perm.permissions.can_send_animations)
    vgames = convert_to_emoji(v_perm.permissions.can_send_games)
    vinlinebots = convert_to_emoji(v_perm.permissions.can_use_inline_bots)
    vwebprev = convert_to_emoji(v_perm.permissions.can_add_web_page_previews)
    vpolls = convert_to_emoji(v_perm.permissions.can_send_polls)
    vinfo = convert_to_emoji(v_perm.permissions.can_change_info)
    vinvite = convert_to_emoji(v_perm.permissions.can_invite_users)
    vpin = convert_to_emoji(v_perm.permissions.can_pin_messages)

    if v_perm is not None:
        try:
            permission_view_str = ""
            permission_view_str += "<b>CHAT PERMISSION INFO:</b>\n\n"
            permission_view_str += f"<b>📩 Send Messages:</b> {vmsg}\n"
            permission_view_str += f"<b>🎭 Send Media:</b> {vmedia}\n"
            permission_view_str += f"<b>🎴 Send Stickers:</b> {vstickers}\n"
            permission_view_str += f"<b>🎲 Send Animations:</b> {vanimations}\n"
            permission_view_str += f"<b>🎮 Can Play Games:</b> {vgames}\n"
            permission_view_str += f"<b>🤖 Can Use Inline Bots:</b> {vinlinebots}\n"
            permission_view_str += f"<b>🌐 Webpage Preview:</b> {vwebprev}\n"
            permission_view_str += f"<b>🗳 Send Polls:</b> {vpolls}\n"
            permission_view_str += f"<b>ℹ Change Info:</b> {vinfo}\n"
            permission_view_str += f"<b>👥 Invite Users:</b> {vinvite}\n"
            permission_view_str += f"<b>📌 Pin Messages:</b> {vpin}\n"

            await m.edit(permission_view_str)
            await c.send_message(
                PRIVATE_GROUP_ID,
                "#VPERM\n\nCHAT: `{}` (`{}`)".format(
                    message.chat.title, message.chat.id
                ),
            )

        except Exception as e_f:
            await m.edit(f"`Something went wrong!` 🤔\n\n**ERROR:** `{e_f}`")

    return
