import asyncio

from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrogram.client.methods.chats.get_chat_members import Filters as ChatMemberFilters


@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & sudo_filter)
async def pin_message(client, message):
    # First of all check if its a group or not
    if message.chat.type in ['group', 'supergroup']:
        # Here lies the sanity checks
        admins = await bot.get_chat_members(message.chat.id, filter=ChatMemberFilters.ADMINISTRATORS)
        admin_ids = [user.user.id for user in admins]
        me = await bot.get_me()

        # If you are an admin
        if me.id in admin_ids:
            # If you replied to a message so that we can pin it.
            if message.reply_to_message:
                disable_notification = True

                # Let me see if you want to notify everyone. People are gonna hate you for this...
                if len(message.command) >= 2 and message.command[1] in ['alert', 'notify', 'loud']:
                    disable_notification = False

                # Pin the fucking message.
                pinned_event = await bot.pin_chat_message(
                    message.chat.id,
                    message.reply_to_message.message_id,
                    disable_notification=disable_notification
                )
                await message.reply_text("`Pinned message!`", parse_mode="md")
                return

            else:
                # You didn't reply to a message and we can't pin anything. ffs
                await message.reply_text(
                    f"`Reply to a message so that I can pin the god damned thing...`", parse_mode="md")
        else:
            # You have no business running this command.
            await message.reply_text("`I am not an admin here lmao. What am I doing?`", parse_mode="md")
    else:
        # Are you fucking dumb this is not a group ffs.
        await message.reply_text("`This is not a place where I can pin shit.`", parse_mode="md")

    # And of course delete your lame attempt at changing the group picture.
    # RIP you.
    # You're probably gonna get ridiculed by everyone in the group for your failed attempt.
    # RIP.
    await asyncio.sleep(3)
    await message.delete()
