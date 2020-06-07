"""Telegram Ping / Pong Speed
Syntax: .ping"""

import time

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.cust_p_filters import sudo_filter

# -- Constants -- #
ALIVE = "`I'm Alive :3`"
HELP = "CAADAgAD6AkAAowucAABsFGHedLEzeUWBA"
REPO = ("User / Bot is available on GitHub:\n"
        "https://github.com/SkuzzyxD/TelePyroBot")
# -- Constants End -- #


@Client.on_message(Filters.command(["alive", "start"], COMMAND_HAND_LER) & sudo_filter)
async def check_alive(_, message):
    await message.reply_text(ALIVE, parse_mode="md")


@Client.on_message(Filters.command("help", COMMAND_HAND_LER) & sudo_filter)
async def help_me(_, message):
    await message.reply_sticker(HELP)


@Client.on_message(Filters.command("ping", COMMAND_HAND_LER) & sudo_filter)
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("Pinging...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n`{time_taken_s:.3f}` ms", parse_mode="md")


@Client.on_message(Filters.command("repo", COMMAND_HAND_LER) & sudo_filter)
async def repo(_, message):
    await message.reply_text(REPO)
