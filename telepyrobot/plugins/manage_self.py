import os
from pyrogram import Client, filters
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


@Client.on_message(filters.command("unblockpm", COMMAND_HAND_LER) & filters.me)
async def unblock_pm(client, message):
    if len(message.command) == 2:
        user = message.text.split(" ", 1)[1]
        try:
            await client.unblock_user(user)
            await message.edit("`Unblocked User`")
        except Exception as ef:
            await message.edit(f"**Error:**\n`{ef}`")
    elif message.reply_to_message:
        user = message.reply_to_message.from_user.id
        try:
            await client.unblock_user(user)
            await message.edit("`Unblocked User`")
        except Exception as ef:
            await message.edit(f"**Error:**\n`{ef}`")
            return


@Client.on_message(filters.command("blockpm", COMMAND_HAND_LER) & filters.me)
async def block_pm(client, message):
    if len(message.command) == 2:
        user = message.text.split(" ", 1)[1]
        try:
            await client.unblock_user(user)
            await message.edit("`Blocked User`")
        except Exception as ef:
            await message.edit(f"**Error:**\n`{ef}`")
    elif message.reply_to_message:
        user = message.reply_to_message.from_user.id
        try:
            await client.unblock_user(user)
            await message.edit("`Blocked User`")
        except Exception as ef:
            await message.edit(f"**Error:**\n`{ef}`")
            return


@Client.on_message(filters.command("uprofile", COMMAND_HAND_LER) & filters.me)
async def update_profile(client, message):
    update = message.txt.split(" ", 2)
    msgreply = message.reply_to_message
    replytxt = message.reply_to_message.text

    # Set first_name
    if update[1] == "fname":
        if update[2]:
            try:
                await client.update_bio(first_name=f"{update[2]}")
                await message.edit(f"**Updated First name to:**\n`{update[2]}`")
            except Exception as ef:
                await message.edit(f"**Error:**\n`{ef}`")
                return
        elif msgreply and not update[2]:
            try:
                await client.update_bio(first_name=f"{replytxt}")
                await message.edit(f"**Updated First name to:**\n`{replytxt}`")
            except Exception as ef:
                await message.edit(f"**Error:**\n`{ef}`")
                return

    # Set last_name
    elif update[1] == "lname":
        if update[2]:
            try:
                await client.update_bio(last_name=f"{update[2]}")
                await message.edit(f"**Updated Last name to:**\n`{update[2]}`")
            except Exception as ef:
                await message.edit(f"**Error:**\n`{ef}`")
                return
        elif msgreply and not update[2]:
            try:
                await client.update_bio(last_name=f"{replytxt}")
                await message.edit(f"**Updated Last name to:**\n`{replytxt}`")
            except Exception as ef:
                await message.edit(f"**Error:**\n`{ef}`")
                return

    # Remove last_name
    elif update[1] == "rmlname":
        try:
            await client.update_bio(last_name="")
            await message.edit(f"**Removed Last name**")
        except Exception as ef:
            await message.edit(f"**Error:**\n`{ef}`")
            return

    # Set bio
    elif update[1] == "bio":
        if update[2]:
            try:
                await client.update_bio(bio=f"{update[2]}")
                await message.edit(f"**Updated Bio**")
            except Exception as ef:
                await message.edit(f"**Error:**\n`{ef}`")
                return
        elif msgreply and not update[2]:
            try:
                await client.update_bio(bio=f"{replytxt}")
                await message.edit(f"**Updated Bio to replied message**")
            except Exception as ef:
                await message.edit(f"**Error:**\n`{ef}`")
                return


@Client.on_message(filters.command("setusername", COMMAND_HAND_LER) & filters.me)
async def set_username(client, message):
    username = message.txt.split(" ", 1)
    if " " in username:
        await message.edit("`Username cannot contain spaces`")
        return
    try:
        await client.update_username(f"{username}")
        await message.edit(f"**Updated Username to:**\n@{username}")
    except Exception as ef:
        await message.edit(f"**Error:**\n{ef}")
        return


@Client.on_message(filters.command("rmusername", COMMAND_HAND_LER) & filters.me)
async def remove_username(client, message):
    try:
        await client.update_username("")
        await message.edit(f"**Removed Username**")
    except Exception as ef:
        await message.edit(f"**Error:**\n{ef}")
        return


@Client.on_message(filters.command("rmpfp", COMMAND_HAND_LER) & filters.me)
async def remove_pfp(client, message):
    photos = client.get_profile_photos("me")
    try:
        client.delete_profile_photos([p.file_id for p in photos[1:]])
        await message.edit(f"**Removed Profile Pictures**")
    except Exception as ef:
        await message.edit(f"**Error:**\n{ef}")
        return
