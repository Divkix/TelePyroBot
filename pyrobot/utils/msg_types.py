from enum import IntEnum, unique

from pyrogram import Message

from pyrobot.utils.string_handling import button_markdown_parser


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


def get_note_type(msg: Message, split: int):
    data_type = None
    content = None
    text = ""
    raw_text = msg.text or msg.caption
    args = raw_text.split(None, split)
    # use python's maxsplit to separate cmd and args
    note_name = args[1]

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if len(args) >= (split + 1) and not msg.reply_to_message:
        text, buttons = button_markdown_parser(msg)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    elif msg.reply_to_message:
        if len(args) >= split and msg.reply_to_message.text:  # not caption, text
            text, buttons = button_markdown_parser(msg.reply_to_message)
            if buttons:
                data_type = Types.BUTTON_TEXT
            else:
                data_type = Types.TEXT

        elif msg.reply_to_message.sticker:
            content = msg.reply_to_message.sticker.file_id
            # stickers can't "officially" have captions in Telegram
            text, buttons = button_markdown_parser(msg)
            data_type = Types.STICKER

        elif msg.reply_to_message.document:
            content = msg.reply_to_message.document.file_id
            text, buttons = button_markdown_parser(msg.reply_to_message)
            data_type = Types.DOCUMENT

        elif msg.reply_to_message.photo:
            content = msg.reply_to_message.photo.file_id
            text, buttons = button_markdown_parser(msg.reply_to_message)
            data_type = Types.PHOTO

        elif msg.reply_to_message.audio:
            content = msg.reply_to_message.audio.file_id
            text, buttons = button_markdown_parser(msg.reply_to_message)
            data_type = Types.AUDIO

        elif msg.reply_to_message.voice:
            content = msg.reply_to_message.voice.file_id
            text, buttons = button_markdown_parser(msg.reply_to_message)
            data_type = Types.VOICE

        elif msg.reply_to_message.video:
            content = msg.reply_to_message.video.file_id
            text, buttons = button_markdown_parser(msg.reply_to_message)
            data_type = Types.VIDEO

        elif msg.reply_to_message.video_note:
            content = msg.reply_to_message.video_note.file_id
            # video notes can never have captions in Telegram
            text, buttons = button_markdown_parser(msg)
            data_type = Types.VIDEO_NOTE

    if split == 1 and note_name == "False":
        note_name = False

    return note_name, text, data_type, content, buttons


def get_file_id(msg: Message):
    data_type = None
    content = None
    if msg.media:
        if msg.sticker:
            content = msg.sticker.file_id
            data_type = Types.STICKER

        elif msg.document:
            content = msg.document.file_id
            data_type = Types.DOCUMENT

        elif msg.photo:
            content = msg.photo.file_id
            data_type = Types.PHOTO
            
        elif msg.audio:
            content = msg.audio.file_id
            data_type = Types.AUDIO
            
        elif msg.voice:
            content = msg.voice.file_id
            data_type = Types.VOICE
            
        elif msg.video:
            content = msg.video.file_id
            data_type = Types.VIDEO
            
        elif msg.video_note:
            content = msg.video_note.file_id
            data_type = Types.VIDEO_NOTE
    return data_type, content


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