from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
import random
import os
# CONSTANTS
DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
RUN_STRINGS = (
    "`Run bc run`",
    "`Bhaag bsdk`",
    "`Hahahaha Lodu bsdk`",
    "`Mc gaand maar dunga`",
    "`Saale chakke`",
    "`Bhag Madarchod`",
    "`Bahut bada chutiya hai tu`")
# CONSTANTS

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
{COMMAND_HAND_LER}throw \ dart Throw an Animated Dart.

{COMMAND_HAND_LER}roll \ dice Throw an Animated Dice.

{COMMAND_HAND_LER}run \ runs Check and watch yourself.
"""


@Client.on_message(Filters.command(["throw", "dart"], COMMAND_HAND_LER) & Filters.me)
async def throw_dart(client, message):
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
    await client.send_dice(
        chat_id=message.chat.id,
        emoji=DART_E_MOJI,
        disable_notification=True,
        reply_to_message_id=rep_mesg_id)


@Client.on_message(Filters.command(["roll", "dice"], COMMAND_HAND_LER) & Filters.me)
async def roll_dice(client, message):
    """ Roll A Dice """
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
    await client.send_dice(
        chat_id=message.chat.id,
        emoji=DICE_E_MOJI,
        disable_notification=True,
        reply_to_message_id=rep_mesg_id)


@Client.on_message(Filters.command(["runs", "run"], COMMAND_HAND_LER) & Filters.me)
async def runs(_, message):
    """ /runs strings """
    run = random.choice(RUN_STRINGS)
    if message.reply_to_message:
        await message.reply_to_message.reply_text(run)
    else:
        await message.reply_text(run)
