import random

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter

RUN_STRINGS = (
    "Run bc run",
    "Bhaag bsdk",
    "Hahahaha Lodu bsdk",
    "Mc gaand maar dunga",
    "Saale chakke",
    "Bhag Madarchod",
    "Bahut bada chutiya hai tu"
)


@Client.on_message(Filters.command("runs", COMMAND_HAND_LER) & sudo_filter)
async def runs(_, message):
    """ /runs strings """
    effective_string = random.choice(RUN_STRINGS)
    if message.reply_to_message:
        await message.reply_to_message.reply_text(effective_string)
    else:
        await message.reply_text(effective_string)
