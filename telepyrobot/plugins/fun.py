from telepyrobot.__main__ import TelePyroBot
from telepyrobot.utils.pyrohelpers import ReplyCheck
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
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
    "`Bahut bada chutiya hai tu`",
    "`Andi mandi shandi, tu bahut bda randi!`",
    "`Aaja mkl tujhe tameez sikahu`",
    "`Baap se bakchodi nahi`",
    "`Kyu? phat gyi gaand?`",
    "`bsdkcunt, jaa gaand mara`",
    "`Lodu saala`",
    "`Kha se aate hai aise log?`" "`Baap se Bakchodi nhi bkl!`",
)
# CONSTANTS

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Just for fun ;)

`{COMMAND_HAND_LER}throw` / dart Throw an Animated Dart.

`{COMMAND_HAND_LER}roll` / dice Throw an Animated Dice.

`{COMMAND_HAND_LER}run` / runs Check and watch yourself.
"""


@TelePyroBot.on_message(
    filters.command(["throw", "dart"], COMMAND_HAND_LER) & filters.me
)
async def throw_dart(c: TelePyroBot, m: Message):
    await m.delete()
    await c.send_dice(
        chat_id=m.chat.id,
        emoji=DART_E_MOJI,
        disable_notification=True,
        reply_to_message_id=ReplyCheck(m),
    )


@TelePyroBot.on_message(
    filters.command(["roll", "dice"], COMMAND_HAND_LER) & filters.me
)
async def roll_dice(c: TelePyroBot, m: Message):
    await m.delete()
    await c.send_dice(
        chat_id=m.chat.id,
        emoji=DICE_E_MOJI,
        disable_notification=True,
        reply_to_message_id=ReplyCheck(m),
    )


@TelePyroBot.on_message(filters.command(["runs", "run"], COMMAND_HAND_LER) & filters.me)
async def runs(c: TelePyroBot, m: Message):
    run = random.choice(RUN_STRINGS)
    if m.reply_to_message:
        await m.reply_to_message.reply_text(run)
        await m.delete()
    else:
        await m.edit(run)
    return
