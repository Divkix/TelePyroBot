from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
import os
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.msg_types import Types, get_note_type
from telepyrobot.utils.pyrohelpers import ReplyCheck
import asyncio
from telepyrobot.db import notes_db as db


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))
__help__ = f"""
Save a note, get that, even you can delete that note.
This note only avaiable for yourself only!

**Save Note**
`{COMMAND_HAND_LER}save <note>`: Save a note, you can get or delete that later.

**Get Note**
`{COMMAND_HAND_LER}get <note>`: Get that note, if avaiable.

**Delete Note**
`{COMMAND_HAND_LER}clear <note>`: Delete that note, if avaiable.
`{COMMAND_HAND_LER}clearall`: Clears all the notes

**All Notes**
`{COMMAND_HAND_LER}saved` or `{COMMAND_HAND_LER}notes`
Get all your notes, if too much notes, please use this in your saved message instead!

-->**__ANYTHING EXCEPT TEXT IS CURRENTLY NOT SUPPORTED__**<--
"""

GET_FORMAT = {
    Types.TEXT.value: TelePyroBot.send_message,
    Types.DOCUMENT.value: TelePyroBot.send_document,
    Types.PHOTO.value: TelePyroBot.send_photo,
    Types.VIDEO.value: TelePyroBot.send_video,
    Types.STICKER.value: TelePyroBot.send_sticker,
    Types.AUDIO.value: TelePyroBot.send_audio,
    Types.VOICE.value: TelePyroBot.send_voice,
    Types.VIDEO_NOTE.value: TelePyroBot.send_video_note,
    Types.ANIMATION.value: TelePyroBot.send_animation,
    Types.ANIMATED_STICKER.value: TelePyroBot.send_sticker,
    Types.CONTACT: TelePyroBot.send_contact,
}


@TelePyroBot.on_message(filters.command("save", COMMAND_HAND_LER) & filters.me)
async def save_note(c: TelePyroBot, m: Message):

    note_name, text, data_type, content, file_ref = get_note_type(m)

    if not note_name:
        await m.edit_text(
            "```" + m.text + "```\n\nError: You must give a name for this note!"
        )
        return

    if data_type == Types.TEXT:
        teks = text
        if not teks:
            await m.edit_text(
                "```" + m.text + "```\n\nError: There is no text in here!"
            )
            return

    db.save_note(m.from_user.id, note_name, text, data_type, content, file_ref)
    await m.edit_text(f"Saved note `{note_name}`!")


@TelePyroBot.on_message(filters.me & filters.command("get", COMMAND_HAND_LER))
async def get_note(c: TelePyroBot, m: Message):
    if len(m.text.split()) >= 2:
        note = m.text.split()[1]
    else:
        await m.edit_text("`Give me a note tag!`")

    getnotes = db.get_note(m.from_user.id, note)
    if not getnotes:
        await m.edit_text("`This note does not exist!`")
        return

    if getnotes["type"] == Types.TEXT:
        teks = getnotes.get("value")
        if teks:
            await m.edit_text(teks)
    elif getnotes["type"] in (
        Types.STICKER,
        Types.VOICE,
        Types.VIDEO_NOTE,
        Types.CONTACT,
        Types.ANIMATED_STICKER,
    ):
        # type_sent = (GET_FORMAT[getnotes['value']].split("_",1)[1])
        # await GET_FORMAT[getnotes['type']](chat_id=m.chat.id, type_sent=getnotes['file_id'], file_ref=getnotes['file_ref'], reply_to_message_id=ReplyCheck(m))
        await m.edit_text("`Currently not supported!`")
    else:
        """if getnotes.get('value'):
            teks = getnotes.get('value')
        else:
            teks = None
        await GET_FORMAT[getnotes['type']](m.chat.id, getnotes['file_id'], getnotes['file_ref'], caption=teks,
                                               reply_to_message_id=ReplyCheck(m))"""
        await m.edit_text("`Currently not supported!`")
    return


@TelePyroBot.on_message(
    filters.me & filters.command(["notes", "saved"], COMMAND_HAND_LER)
)
async def local_notes(c: TelePyroBot, m: Message):

    getnotes = db.get_all_notes(m.from_user.id)
    if not getnotes:
        await m.edit_text("`There are no notes!`")
        return
    rply = "**__Notes:__**\n"
    for x in getnotes:
        if len(rply) >= 1800:
            await m.reply_text(rply)
            rply = "**__Notes:__**\n"
        rply += f"-> `{x}`\n"

    await m.edit_text(rply)


@TelePyroBot.on_message(filters.me & filters.command("clear", COMMAND_HAND_LER))
async def clear_note(c: TelePyroBot, m: Message):
    if len(m.text.split()) <= 1:
        await m.edit_text(
            f"**What do you want to clear?**\n**Use** `{COMMAND_HAND_LER}help notes` **to check how to use!**"
        )
        return

    note = m.text.split()[1]
    getnote = db.rm_note(m.from_user.id, note)
    if not getnote:
        await m.edit_text("`This note does not exist!`")
        return

    await m.edit_text(f"**Deleted note** `{note}`!")


@TelePyroBot.on_message(
    filters.me & filters.command(["clearall", "clearallnotes"], COMMAND_HAND_LER)
)
async def clear_all_notes(c: TelePyroBot, m: Message):
    getnotes = db.get_all_notes(m.from_user.id)
    if not getnotes:
        await m.edit_text("`There are no notes!`")
        return
    for x in getnotes:
        rmnote = db.rm_note(m.from_user.id, x)
    await m.edit_text("`Cleared All Notes`")
    return


@TelePyroBot.on_message(filters.me & filters.command("numnotes", COMMAND_HAND_LER))
async def get_num_notes(c: TelePyroBot, m: Message):
    num_notes = db.get_num_notes(m.from_user.id)
    await m.edit_text(f"`There are total <u>{num_notes}</u> stored`")
    return
