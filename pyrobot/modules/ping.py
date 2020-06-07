import time

from pyrobot import pyrouserbot, OWNER_ID, COMMAND_HAND_LER
from pyrogram import Filters
from pyrobot.helpers.cust_filters import sudo_filter

# -- Constants -- #
ALIVE = "`I'm Alive :3`"
HELP = "CAADAgAD6AkAAowucAABsFGHedLEzeUWBA"
REPO = ("User / Bot is available on GitHub:\n"
        "https://github.com/SkuzzyxD/TelePyroBot")
# -- Constants End -- #

@pyrouserbot.on_message(Filters.command(["ping"], COMMAND_HAND_LER) & sudo_filter)
async def ping(client, message):
	start_time = time.time()
	await message.edit("🏓 Pong!")
	end_time = time.time()
	ping_time = float(end_time - start_time)
	await message.edit("🏓 Pong!\n⏱ Speed was : {0:.2f}s".format(round(ping_time, 2) % 60))


@pyrouserbot.on_message(Filters.command(["alive", "start"], COMMAND_HAND_LER) & sudo_filter)
async def check_alive(client, message):
    await message.reply_text(ALIVE, parse_mode="md")


@pyrouserbot.on_message(Filters.command("help", COMMAND_HAND_LER) & sudo_filter)
async def help_me(client, message):
    await message.reply_sticker(HELP)


@pyrouserbot.on_message(Filters.command("ping", COMMAND_HAND_LER) & sudo_filter)
async def ping(client, message):
    start_t = time.time()
    rm = await message.reply_text("Pinging...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n`{time_taken_s:.3f}` ms", parse_mode="md")


@pyrouserbot.on_message(Filters.command("repo", COMMAND_HAND_LER) & sudo_filter)
async def repo(client, message):
    await message.reply_text(REPO)
