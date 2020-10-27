import time
import os
from platform import python_version
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters, __version__
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, OWNER_NAME, UB_VERSION, OFFICIAL_UPSTREAM_REPO
from pyrogram.raw.all import layer

# -- Constants -- #
ALIVE_TEXT = (
    "<i><b>TelePyroBot is running!!!</b>\n"
    "<i><b>Owner:</b></i> `{}`\n"
    "<i><b>Pyrogram Version:</b></i> `{} (Layer {})`\n"
    "<i><b>Python Version:</b></i> `{}`\n"
    "<i><b>UserBot Version:</b></i> `{}`\n\n"
    "[Deploy TelePyroBot now]({})\n"
    "More info: @TelePyroBot"
)
REPO = (
    "<b>UserBot is available on GitHub:</b>\n"
    "https://github.com/SkuzzyxD/TelePyroBot\n\n"
    "<b>More info:</b> @Skuzzers"
)
# -- Constants End -- #

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Basic commands of userbot!

`{COMMAND_HAND_LER}alive` / start: Check if bot is alive or not.
`{COMMAND_HAND_LER}ping`: Get pinged.
`{COMMAND_HAND_LER}repo`: Get source of this repo.
`{COMMAND_HAND_LER}id`: Get the ID of the file/user/group.
`{COMMAND_HAND_LER}json`: Get json of the replied message.
"""


@TelePyroBot.on_message(filters.command(["alive", "start"], COMMAND_HAND_LER) & filters.me)
async def check_alive(c: TelePyroBot, m: Message):
    await m.edit_text(
        ALIVE_TEXT.format(
            OWNER_NAME,
            __version__,
            layer,
            python_version(),
            UB_VERSION,
            OFFICIAL_UPSTREAM_REPO,
        ),
        disable_web_page_preview=True,
    )


@TelePyroBot.on_message(filters.command("ping", COMMAND_HAND_LER) & filters.me)
async def ping(c: TelePyroBot, m: Message):
    start_t = time.time()
    rm = await m.edit("Pinging...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await m.edit(f"**Pong!**\n`{time_taken_s:.3f}` ms")


@TelePyroBot.on_message(filters.command("repo", COMMAND_HAND_LER) & filters.me)
async def repo(c: TelePyroBot, m: Message):
    await m.edit(REPO, disable_web_page_preview=True)


@TelePyroBot.on_message(filters.command("id", COMMAND_HAND_LER) & filters.me)
async def get_id(c: TelePyroBot, m: Message):
    file_id = None
    user_id = None

    if m.reply_to_message:
        rep = m.reply_to_message
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
                    user_name = (
                        rep.forward_from.first_name + " " + rep.forward_from.last_name
                    )
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
        await m.edit(
            "User Short Info:\n\n**User ID:** `{}`\n**Name:** `{}`\n**Username:** @{}".format(
                user_id, user_name, username
            )
        )
    elif file_id:
        await m.edit("**File's ID:** `{}`".format(file_id))
    else:
        await m.edit("**This Chat's ID:** `{}`".format(message.chat.id))


@TelePyroBot.on_message(filters.command("json", COMMAND_HAND_LER) & filters.me)
async def jsonify(c: TelePyroBot, m: Message):
    the_real_message = None
    reply_to_id = None

    if m.reply_to_message:
        the_real_message = m.reply_to_message
    else:
        the_real_message = message
    try:
        await m.reply_text(f"<code>{the_real_message}</code>")
    except Exception as e:
        with open("json.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(the_real_message))
        await message.reply_document(
            document="json.text",
            caption=str(e),
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove("json.text")
