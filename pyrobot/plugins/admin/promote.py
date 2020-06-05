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


@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & sudo_filter)
async def promote_usr(client, message):
    chat_id = message.chat.id
    check_user = await client.get_chat_member(message.chat.id, message.from_user.id)
    user_type = check_user.status

    if user_type == "member":
        return
    if user_type == "administrator":
        add_adminperm = check_user.can_promote_members
        if add_adminperm:
            msg_promote = await message.reply_text("`Trying to Promote User.. Hang on!! ⏳`")

            if message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
            else:
                args = message.input_str.split(maxsplit=1)
                if len(args) == 1:
                    user_id = args[0]
                else:
                await message.edit(
                    text="`no valid user_id or message specified,`"
                    "`do .help promote for more info`", del_in=0)
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
                    await client.set_administrator_title(chat_id, user_id)
                    await msg_promote.edit("`👑 Promoted Successfully..`")
                except Exception as ef:
                    await msg_promote.edit(
                        text="`something went wrong! 🤔`\n\n"
                        f"**ERROR:** `{ef}`")
                    return
            else:
                await msg_promote.edit(
                    text=r"`I don't have proper permission to do that! (* ￣︿￣)`")
        return
    return
