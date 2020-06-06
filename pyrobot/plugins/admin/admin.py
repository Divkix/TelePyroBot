import asyncio
from pyrogram import Client, Filters, ChatPermissions
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot.helper_functions.extract_user import extract_user
from pyrobot.helper_functions.admin_check import admin_check


@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & sudo_filter)
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


@Client.on_message(Filters.command("demote", COMMAND_HAND_LER) & sudo_filter)
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


@Client.on_message(Filters.command("ban", COMMAND_HAND_LER) & sudo_filter)
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


@Client.on_message(Filters.command("mute", COMMAND_HAND_LER) & sudo_filter)
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


@Client.on_message(Filters.command(["unmute", "unban"], COMMAND_HAND_LER) & sudo_filter)
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


@Client.on_message(Filters.command("pin", COMMAND_HAND_LER) & sudo_filter)
async def pin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        try:
            rm = await.edit("`Trying to pin message...`")
        except:
            rm = await.reply_text("`Trying to pin message...`")
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


@Client.on_message(Filters.command("unpin", COMMAND_HAND_LER) & sudo_filter)
async def unpin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        try:
            rm = await.edit("`Trying to unpin message...`")
        except:
            rm = await.reply_text("`Trying to unpin message...`")
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.unpin_chat_message(chat_id)
        await rm.edit("`Uninned message!`", parse_mode="md")
