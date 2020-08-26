import os
import shutil
import datetime
import asyncio
from prettytable import PrettyTable
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Check info of cases Covid19 (CoronaVirus) Disease

`{COMMAND_HAND_LER}corona` - for Global Stats.
"""


@Client.on_message(filters.command("covid", COMMAND_HAND_LER) & filters.me)
async def covid(c: Client, m: Message):
    await m.edit("`Processing...`", parse_mode="md")
    cmd = message.text.split(" ", 1)
    if len(cmd) == 1:
        r = requests.get("https://corona.lmao.ninja/v2/all?yesterday=true").json()
        last_updated = datetime.datetime.fromtimestamp(r["updated"] / 1000).strftime(
            "%Y-%m-%d %I:%M:%S"
        )

        ac = PrettyTable()
        ac.header = False
        ac.title = "Global Statistics"
        ac.add_row(["Cases", f"{r['cases']:,}"])
        ac.add_row(["Cases Today", f"{r['todayCases']:,}"])
        ac.add_row(["Deaths", f"{r['deaths']:,}"])
        ac.add_row(["Deaths Today", f"{r['todayDeaths']:,}"])
        ac.add_row(["Recovered", f"{r['recovered']:,}"])
        ac.add_row(["Active", f"{r['active']:,}"])
        ac.add_row(["Critical", f"{r['critical']:,}"])
        ac.add_row(["Cases/Million", f"{r['casesPerOneMillion']:,}"])
        ac.add_row(["Deaths/Million", f"{r['deathsPerOneMillion']:,}"])
        ac.add_row(["Tests", f"{r['tests']:,}"])
        ac.add_row(["Tests/Million", f"{r['testsPerOneMillion']:,}"])
        ac.align = "l"
        await m.edit(f"`{str(ac)}`\nLast updated on: {last_updated}", parse_mode="md")
