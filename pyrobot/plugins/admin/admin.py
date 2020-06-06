import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, PyroBot
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot.helper_functions.admin_check import admin_check

@PyroBot.on_message(Filters.command("promote", COMMAND_HAND_LER) & sudo_filter)
async def promote_usr(client, message):
    rm = await message.reply_text("`Trying to Promote User.. Hang on!! ⏳`", parse_mode="md")
    is_admin = await admin_check(message)

    if not is_admin:
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        args = message.input_str.split(maxsplit=1)
        if len(args) == 1:
            user_id = args[0]
        else:
            await rm.edit("`no valid user_id or message specified,`", parse_mode="md")

    if user_id and chat_id:
        try:
            await client.promote_chat_member(chat_id, user_id,
                                            can_change_info=False,
                                            can_delete_messages=True,
                                            can_restrict_members=True,
                                            can_invite_users=True,
                                            can_pin_messages=True)
            await asyncio.sleep(2)
            await rm.edit("`👑 Promoted Successfully..`", parse_mode="md")
        except Exception as ef:
            await rm.edit(
                text="`something went wrong`\n\n"
                f"**ERROR:** `{ef}`", parse_mode="md")


@Client.on_message(Filters.command("demote", COMMAND_HAND_LER) & sudo_filter)
async def demote_usr(client, message):
    rm = await message.reply_text("`Trying to Demote User.. Hang on!! ⏳`", parse_mode="md")
    is_admin = await admin_check(message)

    if not is_admin:
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        args = message.input_str.split(maxsplit=1)
        if len(args) == 1:
            user_id = args[0]
        else:
            await rm.edit("`no valid user_id or message specified`", parse_mode="md")

    if user_id and chat_id:
        try:
            await client.promote_chat_member(chat_id, user_id,
                                            can_change_info=False,
                                            can_delete_messages=False,
                                            can_restrict_members=False,
                                            can_invite_users=False,
                                            can_pin_messages=False)
            await asyncio.sleep(2)
            await rm.edit("`Demoted Successfully..`", parse_mode="md")
        except Exception as ef:
            await rm.edit(
                text="`something went wrong`\n\n"
                f"**ERROR:** `{ef}`", parse_mode="md")
