import requests
import heroku3
import asyncio
import math
from pyrobot import COMMAND_HAND_LER, HEROKU_API_KEY, HEROKU_APP_NAME
from pyrogram import Client, Filters
import os

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Get information about your Heroku Account!
or even restart your dynos from telegram easily!

`{COMMAND_HAND_LER}restart`: Restart userbot heroku dyno.
`{COMMAND_HAND_LER}dynostats`: To get heroku dyno usage.
`{COMMAND_HAND_LER}getvar <Var name>`: Get value of Specified Variable from heroku.
"""

heroku_api = "https://api.heroku.com"
useragent = (
            'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/80.0.3987.149 Mobile Safari/537.36'
            )

@Client.on_message(Filters.command("restart", COMMAND_HAND_LER) & Filters.me)
async def restart(client, message):
    if (HEROKU_API_KEY or HEROKU_APP_NAME) is None:
        await message.edit("Please add `HEROKU_APP_NAME` or `HEROKU_API_KEY` in your Config Vars or file.")
        return
    heroku_conn = heroku3.from_key(HEROKU_API_KEY)
    telepyrobot_app = heroku_conn.apps()[HEROKU_APP_NAME]
    await message.edit("Restarted...!")
    telepyrobot_app.restart()
    return

@Client.on_message(Filters.command("dynostats", COMMAND_HAND_LER) & Filters.me)
async def dynostats(client, message):
    msg = await message.reply_text(
        "Processing...!\n")

    u_id = Heroku.account().id
    if HEROKU_API_KEY is not None:
        headers = {
         'User-Agent': useragent,
         'Authorization': f'Bearer {HEROKU_API_KEY}',
         'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
                }

        path = "/accounts/" + u_id + "/actions/get-quota"
        r = requests.get(heroku_api + path, headers=headers)
        if r.status_code != 200:
            await msg.edit("`Error: something bad happened`\n\n"
                                   f">.`{r.reason}`\n")
        result = r.json()
        quota = result['account_quota']
        quota_used = result['quota_used']

        """ - Used - """
        remaining_quota = quota - quota_used
        percentage = math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)

        """ - Current - """
        App = result['apps']
        try:
            App[0]['quota_used']
        except IndexError:
            AppQuotaUsed = 0
            AppPercentage = 0
        else:
            AppQuotaUsed = App[0]['quota_used'] / 60
            AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)

        await asyncio.sleep(2)

        await msg.reply("**Dyno Usage**:\n\n"
                               f" **--> Dyno usage for App** `{HEROKU_APP_NAME}`:\n"
                               f"\r• `{AppHours}h {AppMinutes}m`"
                               f"**|**  [`{AppPercentage}`**%**]\n"
                               " **--> Dyno hours quota remaining this month:**\n"
                               f"\r• `{hours}h  {minutes}m`"
                               f"**|**  [`{percentage}%`]")

@Client.on_message(Filters.command("vars", COMMAND_HAND_LER) & Filters.me)
async def hetoku_vars(client, message):
    if (HEROKU_API_KEY or HEROKU_APP_NAME) is None:
        await message.edit("Please add `HEROKU_APP_NAME` or `HEROKU_API_KEY` in your Config Vars or file.")
        return
    await message.edit("**__Fetching all vars from Heroku__**")
    heroku_conn = heroku3.from_key(HEROKU_API_KEY)
    telepyrobot_app = heroku_conn.apps()[HEROKU_APP_NAME]
    config = telepyrobot_app.config()
    vars_dict = config.to_dict()
    vars_keys = list(vars_dict.keys())
    msg = "**Here are vars setup for TelePyroBot**\n\n"
    num = 0
    for i in vars_keys:
        num += 1
        msg += f"**{num}**: `{i}`\n"

    msg += f"\n**Total <u>{num}</u> Vars are setup!**"
    await message.edit(msg)
    return
