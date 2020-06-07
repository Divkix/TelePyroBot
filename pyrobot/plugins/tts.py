import os
from gtts import gTTS
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.cust_p_filters import sudo_filter

@Client.on_message(Filters.command("tts", COMMAND_HAND_LER) & sudo_filter)
async def tts(client, message):
    global lang
    if len(message.text.split()) == 1:
        await message.edit("Send text then change to audio")
        return
    await message.delete()
    await client.send_chat_action(message.chat.id, "record_audio")
    text = message.text.split(None, 1)[1]
    tts = gTTS(text, lang=lang)
    tts.save('pyrobot/cache/voice.mp3')
    if message.reply_to_message:
        await client.send_voice(message.chat.id, voice="pyrobot/cache/voice.mp3",
                                reply_to_message_id=message.reply_to_message.message_id)
    else:
        await client.send_voice(message.chat.id, voice="pyrobot/cache/voice.mp3")
    await client.send_chat_action(message.chat.id, action="cancel")
    os.remove("pyrobot/cache/voice.mp3")


@Client.on_message(Filters.command("ttslang", COMMAND_HAND_LER) & sudo_filter)
async def ttslang(client, message):
    global lang
    temp = lang
    lang = message.text.split(None, 1)[1]
    try:
        tts = gTTS("tes", lang=lang)
    except:
        await message.edit("Wrong Language id !")
        lang = temp
        return
    await message.edit("Language Set to {}".format(lang))
