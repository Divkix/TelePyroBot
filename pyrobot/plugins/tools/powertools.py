import requests
from pyrobot import COMMAND_HAND_LER
from pyrogram import Client, Filters
from pyrobot.helper_functions.cust_p_filters import sudo_filter

@Client.on_message(Filters.command("restart", COMMAND_HAND_LER) & sudo_filter)
async def updater(client, message):
    url = 'https://api.heroku.com/apps/telepyrobot/dynos/worker'
    H = {"Accept":"application/vnd.heroku+json; version=3",
"Authorization":"Bearer 72ea0c75-1de5-4938-8040-cd32b6019312" }
    res = requests.delete(url, headers = H)
    await message.reply_text(
        "Restarted! "
        f"Do `{COMMAND_HAND_LER}alive` or `{COMMAND_HAND_LER}start` to check if I am online...", parse_mode="md")
