import time
import os
from platform import python_version
from pyrogram import Client, Filters, __version__
from pyrobot import COMMAND_HAND_LER, OWNER_NAME
from pyrogram.api.all import layer
from pyrobot.utils.extract_user import extract_user

# -- Constants -- #
ALIVE = f"`I'm Alive :3`\n<b>My Owner:</b> `{OWNER_NAME}`\n<b>Pyrogram Version:</b> `{__version__} (Layer {layer})`\n<b>Python Version:</b> `{python_version()}`\nJoin @MyAwesomeProjects for more epic shit!\n\n**Repo Link:**\n[Github](https://github.com/SkuzzyxD/TelePyroBot)"
REPO = ("<b>UserBot is available on GitHub:</b>\n"
        "https://github.com/SkuzzyxD/TelePyroBot\n\n"
        "More info available at: @MyAwesomeProjects")
# -- Constants End -- #

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}alive` \ start: Check if bot is alive or not.

`{COMMAND_HAND_LER}ping`: Get pinged.

`{COMMAND_HAND_LER}repo`: Get source of this repo.

`{COMMAND_HAND_LER}id`: Get the ID of the file/user/group.
Usage: {COMMAND_HAND_LER}id (as a reply to file or user or run to get group id)

`{COMMAND_HAND_LER}json`: Get json of the replied message.
"""

@Client.on_message(Filters.command(["alive", "start"], COMMAND_HAND_LER) & Filters.me)
async def check_alive(client, message):
    await message.edit_text(ALIVE, disable_web_page_preview=True)


@Client.on_message(Filters.command("ping", COMMAND_HAND_LER) & Filters.me)
async def ping(client, message):
    start_t = time.time()
    rm = await message.edit("Pinging...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await message.edit(f"**Pong!**\n`{time_taken_s:.3f}` ms")


@Client.on_message(Filters.command("repo", COMMAND_HAND_LER) & Filters.me)
async def repo(client, message):
    await message.edit(REPO, disable_web_page_preview=True)

@Client.on_message(Filters.command("id", COMMAND_HAND_LER) & Filters.me)
async def get_id(client, message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message
        if rep.audio:
            file_id = rep.audio.file_id
        elif rep.document:
            file_id = rep.document.file_id
        elif rep.photo:
            file_id = rep.photo.file_id
        elif rep.sticker:
            file_id = rep.sticker.file_id
        elif rep.video:
            file_id = rep.video.file_id
        elif rep.animation:
            file_id = rep.animation.file_id
        elif rep.voice:
            file_id = rep.voice.file_id
        elif rep.video_note:
            file_id = rep.video_note.file_id
        elif rep.contact:
            file_id = rep.contact.file_id
        elif rep.location:
            file_id = rep.location.file_id
        elif rep.venue:
            file_id = rep.venue.file_id
        elif rep.from_user:
            if rep.forward_from:
                user_id = rep.forward_from.id
                if rep.forward_from.last_name:
                    user_name = rep.forward_from.first_name + " " + rep.forward_from.last_name
                else:
                    user_name = rep.forward_from.first_name
                username = rep.forward_from.username
            else:
                user_id = rep.from_user.id
                if rep.from_user.last_name:
                    user_name = rep.from_user.first_name + " " + rep.from_user.last_name
                else:
                    user_name = rep.from_user.first_name
                username = rep.from_user.username

    if user_id:
        await message.edit("User Short Info:\n\n**User ID:** `{}`\n**Name:** `{}`\n**Username:** @{}".format(user_id, user_name, username))
    elif file_id:
        await message.edit("**File's ID:** `{}`".format(file_id))
    else:
        await message.edit("**This Chat's ID:** `{}`".format(message.chat.id))


@Client.on_message(Filters.command("json", COMMAND_HAND_LER) & Filters.me)
async def jsonify(client, message):
    the_real_message = None
    reply_to_id = None

    if message.reply_to_message:
        the_real_message = message.reply_to_message
    else:
        the_real_message = message
    try:
        await message.reply_text(f"<code>{the_real_message}</code>")
    except Exception as e:
        with open("json.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(the_real_message))
        await message.reply_document(
            document="json.text",
            caption=str(e),
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("json.text")
