import os
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, LOGGER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
A module to manage your own user account.

__**Commands:**__
**Block User:** `{COMMAND_HAND_LER}blockpm <user_id or username>` or as a reply to user
Unblocks the user, if you blocked.

**Unblock User:** `{COMMAND_HAND_LER}unblockpm <user_id or username>` or as a reply to user
Blocks the user, if you blocked it.

**Update Profile:**
{COMMAND_HAND_LER}uprofile fname / lname / rmlname / Bio

**Usage:**
`{COMMAND_HAND_LER}uprofile fname <first name>`: sets you firstname to specified text or to text of replied message.
`{COMMAND_HAND_LER}uprofile lname <last name>`: sets you lastname to specified text or to text of replied message.
`{COMMAND_HAND_LER}uprofile bio <bio>`: sets you bio to specified text or to text of replied message.
`{COMMAND_HAND_LER}uprofile rmlname`: removes your lastname.

**Update Username**
`{COMMAND_HAND_LER}setusername <username>`: Sets your username to specified username.
`{COMMAND_HAND_LER}rmusername`: Removes your username

**Profile Pictures**
`{COMMAND_HAND_LER}rmpfp`: Removes all your profile pictures.
"""


@TelePyroBot.on_message(filters.command("unblockpm", COMMAND_HAND_LER) & filters.me)
async def unblock_pm(c: TelePyroBot, m: Message):
    if len(m.command) == 2:
        user = m.text.split(None, 1)[1]
        try:
            await c.unblock_user(user)
            await m.edit_text("`Unblocked User`")
        except Exception as ef:
            await m.edit_text(f"**Error:**\n`{ef}`")
    elif m.reply_to_message:
        user = m.reply_to_message.from_user.id
        try:
            await c.unblock_user(user)
            await m.edit_text("`Unblocked User`")
        except Exception as ef:
            await m.edit_text(f"**Error:**\n`{ef}`")
    return


@TelePyroBot.on_message(filters.command("blockpm", COMMAND_HAND_LER) & filters.me)
async def block_pm(c: TelePyroBot, m: Message):
    if len(m.command) == 2:
        user = m.text.split(None, 1)[1]
        try:
            await c.unblock_user(user)
            await m.edit_text("`Blocked User`")
        except Exception as ef:
            await m.edit_text(f"**Error:**\n`{ef}`")
    elif m.reply_to_message:
        user = m.reply_to_message.from_user.id
        try:
            await c.unblock_user(user)
            await m.edit_text("`Blocked User`")
        except Exception as ef:
            await m.edit_text(f"**Error:**\n`{ef}`")
    return


@TelePyroBot.on_message(filters.command("uprofile", COMMAND_HAND_LER) & filters.me)
async def update_profile(c: TelePyroBot, m: Message):
    update = m.text.split(None, 2)
    msgreply = m.reply_to_message
    replytxt = m.reply_to_message.text

    # Set first_name
    if update[1] == "fname":
        if update[2]:
            try:
                await c.update_bio(first_name=f"{update[2]}")
                await m.edit_text(f"**Updated First name to:**\n`{update[2]}`")
            except Exception as ef:
                await m.edit_text(f"**Error:**\n`{ef}`")
                return
        elif msgreply and not update[2]:
            try:
                await c.update_bio(first_name=f"{replytxt}")
                await m.edit_text(f"**Updated First name to:**\n`{replytxt}`")
            except Exception as ef:
                await m.edit_text(f"**Error:**\n`{ef}`")
                return

    # Set last_name
    elif update[1] == "lname":
        if update[2]:
            try:
                await c.update_bio(last_name=f"{update[2]}")
                await m.edit_text(f"**Updated Last name to:**\n`{update[2]}`")
            except Exception as ef:
                await m.edit_text(f"**Error:**\n`{ef}`")
                return
        elif msgreply and not update[2]:
            try:
                await c.update_bio(last_name=f"{replytxt}")
                await m.edit_text(f"**Updated Last name to:**\n`{replytxt}`")
            except Exception as ef:
                await m.edit_text(f"**Error:**\n`{ef}`")
                return

    # Remove last_name
    elif update[1] == "rmlname":
        try:
            await c.update_bio(last_name="")
            await m.edit_text(f"**Removed Last name**")
        except Exception as ef:
            await m.edit_text(f"**Error:**\n`{ef}`")
            return

    # Set bio
    elif update[1] == "bio":
        if update[2]:
            try:
                await c.update_bio(bio=f"{update[2]}")
                await m.edit_text(f"**Updated Bio**")
            except Exception as ef:
                await m.edit_text(f"**Error:**\n`{ef}`")
                return
        elif msgreply and not update[2]:
            try:
                await c.update_bio(bio=f"{replytxt}")
                await m.edit_text(f"**Updated Bio to replied message**")
            except Exception as ef:
                await m.edit_text(f"**Error:**\n`{ef}`")
    return


@TelePyroBot.on_message(filters.command("setusername", COMMAND_HAND_LER) & filters.me)
async def set_username(c: TelePyroBot, m: Message):
    username = m.text.split(None, 1)
    if " " in username:
        await m.edit_text("`Username cannot contain spaces`")
        return
    try:
        await c.update_username(f"{username}")
        await m.edit_text(f"**Updated Username to:**\n@{username}")
    except Exception as ef:
        await m.edit_text(f"**Error:**\n{ef}")
    return


@TelePyroBot.on_message(filters.command("rmusername", COMMAND_HAND_LER) & filters.me)
async def remove_username(c: TelePyroBot, m: Message):
    try:
        await c.update_username("")
        await m.edit_text(f"**Removed Username**")
    except Exception as ef:
        await m.edit_text(f"**Error:**\n{ef}")
    return


@TelePyroBot.on_message(filters.command("rmpfp", COMMAND_HAND_LER) & filters.me)
async def remove_pfp(c: TelePyroBot, m: Message):
    photos = c.get_profile_photos("me")
    try:
        c.delete_profile_photos([p.file_id for p in photos[1:]])
        await m.edit_text(f"**Removed Profile Pictures**")
    except Exception as ef:
        await m.edit_text(f"**Error:**\n{ef}")
    return
