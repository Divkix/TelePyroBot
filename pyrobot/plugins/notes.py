from pyrogram import Filters, Client

from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.msg_types import Types, get_note_type
from pyrobot.utils.pyrohelpers import ReplyCheck

from pyrobot.utils.sql_helpers import notes_db as db


__PLUGIN__ = "notes"
__HELP__ = """
Save a note, get that, even you can delete that note.
This note only avaiable for yourself only!
Also notes support inline button powered by inline query assistant bot.

──「 **Save Note** 」──
-> `save (note)`
Save a note, you can get or delete that later.

──「 **Get Note** 」──
-> `get (note)`
Get that note, if avaiable.

──「 **Delete Note** 」──
-> `clear (note)`
Delete that note, if avaiable.

──「 **All Notes** 」──
-> `saved`
-> `notes`
Get all your notes, if too much notes, please use this in your saved message instead!


── **Note Format** ──
-> **Button**
`[Button Text](buttonurl:google.com)`
-> **Bold**
`**Bold**`
-> __Italic__
`__Italic__`
-> `Code`
`Code` (grave accent)
"""

GET_FORMAT = {
    Types.TEXT.value: Client.send_message,
    Types.DOCUMENT.value: Client.send_document,
    Types.PHOTO.value: Client.send_photo,
    Types.VIDEO.value: Client.send_video,
    Types.STICKER.value: Client.send_sticker,
    Types.AUDIO.value: Client.send_audio,
    Types.VOICE.value: Client.send_voice,
    Types.VIDEO_NOTE.value: Client.send_video_note,
    Types.ANIMATION.value: Client.send_animation,
    Types.ANIMATED_STICKER.value: Client.send_sticker,
    Types.CONTACT: Client.send_contact
}


@Client.on_message(Filters.command("save", COMMAND_HAND_LER) & Filters.me)
async def save_note(client, message):
    note_name, text, data_type, content = get_note_type(message)

    if not note_name:
        await message.edit("```" + message.text + '```\n\nError: You must give a name for this note!')
        return

    if data_type == Types.TEXT:
        teks = text
        if not teks:
            await message.edit("```" + message.text + '```\n\nError: There is no text in here!')
            return

    db.save_selfnote(message.from_user.id, note_name, text, data_type, content)
    await message.edit(f'Saved note `{note_name}`!')


@Client.on_message(Filters.me & Filters.command("get", COMMAND_HAND_LER))
async def get_note(client, message):
    if len(message.text.split()) >= 2:
        note = message.text.split()[1]
    else:
        await message.edit("Give me a note tag!")

    getnotes = db.get_selfnote(message.from_user.id, note)
    if not getnotes:
        await message.edit("This note does not exist!")
        return

    if getnotes['type'] == Types.TEXT:
        teks = getnotes.get('value')
        if teks:
            await message.edit(teks)
    elif getnotes['type'] in (Types.STICKER, Types.VOICE, Types.VIDEO_NOTE, Types.CONTACT, Types.ANIMATED_STICKER):
        await GET_FORMAT[getnotes['type']](message.chat.id, getnotes['file'], reply_to_message_id=ReplyCheck(message))
    else:
        await message.edit("`Non supported format!`")

@Client.on_message(Filters.me & Filters.command(["notes", "saved"], COMMAND_HAND_LER))
async def local_notes(_client, message):
    getnotes = db.get_all_selfnotes(message.from_user.id)
    if not getnotes:
        await message.edit("There are no notes in local notes!")
        return
    rply = "**Local notes:**\n"
    for x in getnotes:
        if len(rply) >= 1800:
            await message.reply(rply)
            rply = "**Local notes:**\n"
        rply += f"- `{x}`\n"

    await message.edit(rply)


@Client.on_message(Filters.me & Filters.command("clear", COMMAND_HAND_LER))
async def clear_note(_client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    if len(message.text.split()) <= 1:
        await message.edit("What do you want to clear?")
        return

    note = message.text.split()[1]
    getnote = db.rm_selfnote(message.from_user.id, note)
    if not getnote:
        await message.edit("This note does not exist!")
        return

    await message.edit(f"Deleted note `{note}`!")
