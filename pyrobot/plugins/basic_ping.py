"""Basic Commands"""

import time
import os
from pyrogram import Client, Filters, __version__
from pyrobot import COMMAND_HAND_LER, OWNER_NAME
from pyrogram.api.all import layer
from pyrobot.utils.extract_user import extract_user

# -- Constants -- #
ALIVE = f"`I'm Alive :3`\n<b>My Owner:</b> `{OWNER_NAME}`\n<b>Python Version:</b> `3.6.10`\n<b>Pyrogram Version:</b> `{__version__} (Layer {layer})`"
HELP = "CAADAgAD6AkAAowucAABsFGHedLEzeUWBA"
REPO = ("<b>UserBot is available on GitHub:</b>\n"
        "https://github.com/SkuzzyxD/TelePyroBot")
# -- Constants End -- #


@Client.on_message(Filters.command(["alive", "start"], COMMAND_HAND_LER) & Filters.me)
async def check_alive(client, message):
    me = await client.get_me()
    name = me.first_name
    if me.last_name:
        name = me.first_name + ' ' + me.last_name
    if me.username:
        username = me.username
    await message.edit_text(ALIVE)


@Client.on_message(Filters.command("help", COMMAND_HAND_LER) & Filters.me)
async def help_me(client, message):
    await message.reply_sticker(HELP)


@Client.on_message(Filters.command("ping", COMMAND_HAND_LER) & Filters.me)
async def ping(client, message):
    start_t = time.time()
    rm = await message.edit("Pinging...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await message.edit(f"Pong!\n`{time_taken_s:.3f}` ms")


@Client.on_message(Filters.command("repo", COMMAND_HAND_LER) & Filters.me)
async def repo(client, message):
    await message.edit(REPO)

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
            user_id = rep.from_user.id

    if user_id:
        await message.edit("This User's ID: `{}`".format(user_id))
    elif file_id:
        await message.edit("This File's ID: `{}`".format(file_id))
    else:
        await message.edit("This Chat's ID:\n`{}`".format(message.chat.id))


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