from enum import IntEnum, unique
from pyrogram import Message

@unique
class Types(IntEnum):
    TEXT = 1
    DOCUMENT = 2
    PHOTO = 3
    VIDEO = 4
    STICKER = 5
    AUDIO = 6
    VOICE = 7
    VIDEO_NOTE = 8
    ANIMATION = 9
    ANIMATED_STICKER = 10
    CONTACT = 11

def get_message_type(msg):
    if msg.text or msg.caption:
        content = None
        message_type = Types.TEXT
    elif msg.sticker:
        content = msg.sticker.file_id
        message_type = Types.STICKER

    elif msg.document:
        if msg.document.mime_type == "application/x-bad-tgsticker":
            message_type = Types.ANIMATED_STICKER
        else:
            message_type = Types.DOCUMENT
        content = msg.document.file_id

    elif msg.photo:
        content = msg.photo.file_id  # last elem = best quality
        message_type = Types.PHOTO

    elif msg.audio:
        content = msg.audio.file_id
        message_type = Types.AUDIO

    elif msg.voice:
        content = msg.voice.file_id
        message_type = Types.VOICE

    elif msg.video:
        content = msg.video.file_id
        message_type = Types.VIDEO

    elif msg.video_note:
        content = msg.video_note.file_id
        message_type = Types.VIDEO_NOTE

    elif msg.animation:
        content = msg.animation.file_id
        message_type = Types.ANIMATION

    else:
        return None, None

    return content, message_type


def get_note_type(msg):
    if len(msg.text.split()) <= 1:
        return None, None, None, None
    data_type = None
    content = None
    raw_text = msg.text.markdown if msg.text else msg.caption.markdown
    args = raw_text.split(None, 2)  # use python's maxsplit to separate cmd and args
    note_name = args[1]

    # determine what the contents of the filter are - text, image, sticker, etc
    if len(args) >= 3:
        text = args[2]
        data_type = Types.TEXT

    elif msg.reply_to_message:
        if msg.reply_to_message.text:
            text = msg.reply_to_message.text.markdown
        elif msg.reply_to_message.caption:
            text = msg.reply_to_message.caption.markdown
        else:
            text = ""
        if len(args) >= 2 and msg.reply_to_message.text:  # not caption, text
            data_type = Types.TEXT

        elif msg.reply_to_message.sticker:
            content = msg.reply_to_message.sticker.file_id
            file_ref = msg.reply_to_message.sticker.file_ref
            data_type = Types.STICKER

        elif msg.reply_to_message.document:
            if msg.reply_to_message.document.mime_type == "application/x-bad-tgsticker":
                data_type = Types.ANIMATED_STICKER
            else:
                data_type = Types.DOCUMENT
            content = msg.reply_to_message.document.file_id
            file_ref = msg.reply_to_message.document.file_ref

        elif msg.reply_to_message.photo:
            content = msg.reply_to_message.photo.file_id  # last elem = best quality
            file_ref = msg.reply_to_message.photo.file_ref
            data_type = Types.PHOTO

        elif msg.reply_to_message.audio:
            content = msg.reply_to_message.audio.file_id
            file_ref = msg.reply_to_message.audio.file_ref
            data_type = Types.AUDIO

        elif msg.reply_to_message.voice:
            content = msg.reply_to_message.voice.file_id
            file_ref = msg.reply_to_message.voice.file_ref
            data_type = Types.VOICE

        elif msg.reply_to_message.video:
            content = msg.reply_to_message.video.file_id
            file_ref = msg.reply_to_message.video.file_ref
            data_type = Types.VIDEO

        elif msg.reply_to_message.video_note:
            content = msg.reply_to_message.video_note.file_id
            file_ref = msg.reply_to_message.video_note.file_ref
            data_type = Types.VIDEO_NOTE

        elif msg.reply_to_message.animation:
            content = msg.reply_to_message.animation.file_id
            file_ref = msg.reply_to_message.animation.file_ref
            data_type = Types.ANIMATION

    else:
        return None, None, None, None, None

    return note_name, text, data_type, content, file_ref
