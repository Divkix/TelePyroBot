from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter


async def is_admin(message: Message):
    check_user = await client.get_chat_member(message.chat.id, message.from_user.id)
    user_type = check_user.status
    if user_type == "member":
        return False
    if user_type == "administrator":
        rm_perm = check_user.can_restrict_members
        if rm_perm:
            return True
        return False
    return True

async def is_sudoadmin(message: Message):
    check_user = await client.get_chat_member(message.chat.id, message.from_user.id)
    user_type = check_user.status
    if user_type == "member":
        return False
    if user_type == "administrator":
        add_adminperm = check_user.can_promote_members
        if add_adminperm:
            return True
        return False
    return True


@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & sudo_filter)
async def promote_usr(client, message):
    custom_rank = ""
    chat_id = message.chat.id
    get_group = await client.get_chat(chat_id)
    can_promo = await is_sudoadmin(message)

    if can_promo:
        msg_promote = await message.reply_text("`Trying to Promote User.. Hang on!! ⏳`")
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            custom_rank = get_emoji_regexp().sub(u'', message.input_str)
            if len(custom_rank) > 15:
                custom_rank = custom_rank[:15]
        else:
            args = message.input_str.split(maxsplit=1)
            if len(args) == 2:
                user_id, custom_rank = args
                custom_rank = get_emoji_regexp().sub(u'', custom_rank)
                if len(custom_rank) > 15:
                    custom_rank = custom_rank[:15]
            elif len(args) == 1:
                user_id = args[0]
            else:
                await edit(
                    text="`no valid user_id or message specified,`")
                return
        if user_id:
            try:
                get_mem = await client.get_chat_member(chat_id, user_id)
                await client.promote_chat_member(chat_id, user_id,
                                                 can_change_info=False,
                                                 can_delete_messages=True,
                                                 can_restrict_members=True,
                                                 can_invite_users=True,
                                                 can_pin_messages=True)
                await asyncio.sleep(2)
                await client.set_administrator_title(chat_id, user_id, custom_rank)
                await msg_promote.edit("`👑 Promoted Successfully..`")

            except Exception as ef:
                await msg_promote.edit(
                    text="`something went wrong! 🤔`\n\n"
                    f"**ERROR:** `{ef}`")
                return
    else:
        await msg_promote.edit(
            text=r"`I don't have proper permission to do that! (* ￣︿￣)`")


@Client.on_message(Filters.command("demote", COMMAND_HAND_LER) & sudo_filter)
async def demote_usr(client, message):
    """
    this function can demote members in tg group
    """
    chat_id = message.chat.id
    get_group = await client.get_chat(chat_id)
    can_demote = await is_sudoadmin(message)

    if can_demote:
        msg_demote = await message.reply_text("`Trying to Demote User.. Hang on!! ⏳`")
        user_id = message.input_str
        if user_id:
            try:
                get_mem = await client.get_chat_member(chat_id, user_id)
                await client.promote_chat_member(chat_id, user_id,
                                                 can_change_info=False,
                                                 can_delete_messages=False,
                                                 can_restrict_members=False,
                                                 can_invite_users=False,
                                                 can_pin_messages=False)
                await msg_demote.edit("`🛡 Demoted Successfully..`")

            except Exception as e_f:
                await msg_demote.edit(
                    text="`something went wrong! 🤔`\n\n"
                    f"**ERROR:** `{e_f}`")
                return

        elif message.reply_to_message:
            try:
                get_mem = await client.get_chat_member(
                    chat_id,
                    message.reply_to_message.from_user.id)
                await client.promote_chat_member(chat_id, get_mem.user.id,
                                                 can_change_info=False,
                                                 can_delete_messages=False,
                                                 can_restrict_members=False,
                                                 can_invite_users=False,
                                                 can_pin_messages=False)

                await msg_demote.edit("`🛡 Demoted Successfully..`")
            except Exception as e_f:
                await msg_demote.edit(
                    text="`something went wrong! 🤔`\n\n"
                    f"**ERROR:** `{e_f}`")
                return
        else:
            await msg_demote.edit(
                text="`no valid user_id or message specified,`")
            return
    else:
        await msg_demote.edit(
            text=r"`I don't have proper permission to do that! (* ￣︿￣)`")
