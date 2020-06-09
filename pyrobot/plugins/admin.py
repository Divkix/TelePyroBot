import asyncio
from pyrogram import Client, Filters, ChatPermissions
from pyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN

from pyrobot.utils.extract_user import extract_user
from pyrobot.utils.admin_check import admin_check


__PLUGIN__ = "Admin"

__help__ = f"""
{COMMAND_HAND_LER}promote: Promotes a user in the Group.
Usage: {COMMAND_HAND_LER}promote (Username/User ID or reply to message)

{COMMAND_HAND_LER}demote: Demotes a user in the Group.
Usage: {COMMAND_HAND_LER}demote (Username/User ID or reply to message)

{COMMAND_HAND_LER}ban: Bans a user in the Group.
Usage: {COMMAND_HAND_LER}ban (Username/User ID or reply to message)

{COMMAND_HAND_LER}mute: Mutes a user in the Group.
Usage: {COMMAND_HAND_LER}mute (Username/User ID or reply to message)

{COMMAND_HAND_LER}demote: Demotes a user in the Group.
Usage: {COMMAND_HAND_LER}demote (Username/User ID or reply to message)

{COMMAND_HAND_LER}unmute \ unban \ unrestrict: Unrestricts a user in the Group.
Usage: {COMMAND_HAND_LER}unmute (Username/User ID or reply to message)

{COMMAND_HAND_LER}pin: Pins the message in the Group.
Usage: {COMMAND_HAND_LER}pin (as a reply to the message)

{COMMAND_HAND_LER}unpin: Pins the message in the Group.
Usage: {COMMAND_HAND_LER}unpin

{COMMAND_HAND_LER}leavechat: Exit from the Group.
Usage: {COMMAND_HAND_LER}leavechat

{COMMAND_HAND_LER}invitelink: Gives the invitelink of the Group.
Usage: {COMMAND_HAND_LER}invitelink

{COMMAND_HAND_LER}setchatpic: Changes the Picture of Group.
Usage: {COMMAND_HAND_LER}setchatpic (as a reply to the message)

{COMMAND_HAND_LER}delchatpic: Removes the Picture of Group.
Usage: {COMMAND_HAND_LER}delchatpic (as a reply to the message)

{COMMAND_HAND_LER}setchatname: Renames the Group.
Usage: {COMMAND_HAND_LER}setchatname (chatname or as a reply to the message)

{COMMAND_HAND_LER}setchatdesc: Sets the Description of the Group.
Usage: {COMMAND_HAND_LER}setchatdesc (chatdesc or as a reply to the message)

{COMMAND_HAND_LER}purge: Deletes messages upto replied message.
Usage: {COMMAND_HAND_LER}purge (as a reply to the message)

{COMMAND_HAND_LER}del: Deletes a single message.
Usage: {COMMAND_HAND_LER}del (as a reply to the message)

{COMMAND_HAND_LER}invite: Sets the Description of the Group.
Usage: {COMMAND_HAND_LER}invite (Username or User ID)
"""


@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & Filters.me)
async def promote_usr(client, message):
    await message.edit("`Trying to Promote User.. Hang on!! ⏳`")
    is_admin = await admin_check(message)

    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)
    chat_id = message.chat.id
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
        await message.edit(f"`👑 Promoted` [{user_first_name}](tg://user?id={user_id}) `Successfully...`")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("demote", COMMAND_HAND_LER) & Filters.me)
async def demote_usr(client, message):
    await message.edit("`Trying to Demote User.. Hang on!! ⏳`")
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    try:
        await client.promote_chat_member(chat_id, user_id,
                                        can_change_info=False,
                                        can_delete_messages=False,
                                        can_restrict_members=False,
                                        can_invite_users=False,
                                        can_pin_messages=False)
        await asyncio.sleep(2)
        await message.edit(f"`Demoted` [{user_first_name}](tg://user?id={user_id}) `Successfully...`")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("ban", COMMAND_HAND_LER) & Filters.me)
async def ban_usr(client, message):
    await message.edit("`Trying to Ban User.. Hang on!! ⏳`")
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.kick_member(user_id)
        await message.edit(f"`Banned` [{user_first_name}](tg://user?id={user_id}) `Successfully...`")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command("mute", COMMAND_HAND_LER) & Filters.me)
async def restrict_usr(client, message):
    await message.edit("`Trying to Mute User.. Hang on!! ⏳`")
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions())
        await message.edit(f"`Muted` [{user_first_name}](tg://user?id={user_id}) `Successfully...`")
    except Exception as ef:
        await message.edit(f"**Error:**\n\n`{ef}`")


@Client.on_message(Filters.command(["unmute", "unban", "unrestrict"], COMMAND_HAND_LER) & Filters.me)
async def unrestrict_usr(client, message):
    await message.edit("`Trying to Unrestrict User.. Hang on!! ⏳`")
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.unban_member(
            user_id=user_id)
        await message.edit(f"`Unrestrict` [{user_first_name}](tg://user?id={user_id}) `Successfully...`")
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


@Client.on_message(Filters.command("leavechat", COMMAND_HAND_LER) & Filters.me)
async def leavechat(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await client.leave_chat(chat_id, delete=True)


@Client.on_message(Filters.command("invitelink", COMMAND_HAND_LER) & Filters.me)
async def invitelink(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    link = await client.export_chat_invite_link(chat_id)
    await message.edit(f"**Link for Chat:**\n`{link}`")


@Client.on_message(Filters.command("setchatpic", COMMAND_HAND_LER) & Filters.me)
async def set_picture(client, message):
    if message.chat.type in ['group', 'supergroup']:
        is_admin = await admin_check(message)
        if not is_admin:
            return
        await message.edit("`Tring to Change Group Picture....`")
        chat_id = message.chat.id
        try:
            if message.reply_to_message and message.reply_to_message.media:
                file_id = message.reply_to_message.photo.file_id
                file_ref = message.reply_to_message.photo.file_ref
                await client.set_chat_photo(chat_id, file_id, file_ref=file_ref)
                await message.edit(f"`{message.chat.type.title()} picture has been set.`")
            else:
                await message.edit("`Reply to an image to set that as group pic`")
        except Exception as ef:
            await message.edit(f"**Could not Change Chat Pic due to:**\n`{ef}`")


@Client.on_message(Filters.command("delchatpic", COMMAND_HAND_LER) & Filters.me)
async def delchatpic(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    try:
        await client.delete_chat_photo(chat_id)
        await message.edit(f"`Deleted Chat Picture for {message.chat.type.title()}`")
    except Exception as ef:
        await message.edit(f"Error deleting Chat Pic due to:\n`{ef}`")


@Client.on_message(Filters.command("setchatname", COMMAND_HAND_LER) & Filters.me)
async def setchatname(client, message):
    await message.edit("__Trying to Change Chat Name!__")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    chat_title = message.text.split(' ', 1)
    if message.reply_to_message:
        chat_title = message.reply_to_message.text
    else:
        chat_title = chat_title[1]
    try:
        await client.set_chat_title(chat_id, chat_title)
        await message.edit(f"<b>Changed Chat Name to:</b> <code>{chat_title}</code>")
    except Exception as ef:
        await message.edit(f"**Could not Change Chat Title due to:**\n`{ef}`")


@Client.on_message(Filters.command("setchatdesc", COMMAND_HAND_LER) & Filters.me)
async def setchatdesc(client, message):
    await message.edit("__Trying to Change Chat Desciption!__")
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    chat_desc = message.text.split(' ', 1)
    if message.reply_to_message:
        chat_desc = message.reply_to_message.text
    else:
        chat_desc = chat_desc[1]
    try:
        await client.set_chat_description(chat_id, chat_desc)
        await message.edit(f"<b>Changed Chat Name to:</b> <code>{chat_desc}</code>")
    except Exception as ef:
        await message.edit(f"**Could not Change Chat Desciption due to:**\n`{ef}`")


@Client.on_message(Filters.command("purge", COMMAND_HAND_LER) & Filters.me)
async def purge(client, message):
    """ purge upto the replied message """
    if message.chat.type in (("supergroup", "channel")):
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

    await message.edit(
        f"Deleted `{count_del_etion_s}` messages")
    await asyncio.sleep(5)
    await message.delete()


@Client.on_message(Filters.command("del", COMMAND_HAND_LER) & Filters.me)
async def del_msg(client, message):
    """ Delete the replied message """
    if message.chat.type in (("supergroup", "channel")):
        is_admin = await admin_check(message)
        if not is_admin:
            return
    chat_id = message.chat.id
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        await client.delete_messages(chat_id, message_id)
        await message.delete()
    else:
        await message.edit("`Reply to a message to delete it!`")
        return


@Client.on_message(Filters.command("invite", COMMAND_HAND_LER) & Filters.me)
async def del_msg(client, message):
    cmd = message.text.split(' ', 1)
    user_id = cmd[1]
    if user_id:
        try:
            from_user = await client.get_users(user_id)
            from_chat = await client.get_chat(user_id)
        except Exception:
            await message.edit("no valid user_id or message specified")
            return
    elif message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
        from_chat = await client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.edit("no valid user_id or message specified")
        return
    try:
        await chat.add_members(user_id)
    except:
        await message.edit("<b>Could not add user, maybe the user has restricted himself from being added to group.</b>")
        return
