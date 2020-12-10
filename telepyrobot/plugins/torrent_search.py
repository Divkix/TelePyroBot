import requests
import json
from io import BytesIO
import asyncio
import os
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY
from telepyrobot.utils.clear_string import clear_string

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Get Magnet Links of any search query.

`{COMMAND_HAND_LER}tsearch <query>`: Search for torrent query and display results.
"""


@TelePyroBot.on_message(filters.command("tsearch", COMMAND_HAND_LER) & filters.me)
async def tor_search(c: TelePyroBot, m: Message):
    if len(m.command) == 1:
        await m.edit_text("`Check help on how to use this command`")
        return
    await m.edit_text("`Please wait, fetching results...`")
    query = m.text.split(None, 1)[1]
    response = requests.get(f"https://api.sumanjay.cf/torrent/?query=ubuntu{query}")
    ts = json.loads(response.text)
    if not ts == response.json():
        await m.edit_text("**Some error occured**\n`Try Again Later`")
        return
    listdata = ""
    run = 0
    while True:
        try:
            run += 1
            r1 = ts[run]
            list1 = "<-----{}----->\nName: {}\nSeeders: {}\nSize: {}\nAge: {}\n<--Magnet Below-->\n{}\n\n\n".format(
                run, r1["name"], r1["seeder"], r1["size"], r1["age"], r1["magnet"]
            )
            listdata = listdata + list1
        except:
            break

    OUTPUT = clear_string(listdata)  # Remove the html elements using regex
    try:
        with BytesIO(str.encode(OUTPUT)) as f:
            f.name = "torrent_search.txt"
            await m.reply_document(
                document=f, caption=f"Here are the results for the query: {query}"
            )
        await m.delete()
    except ValueError:
        await m.edit_text("Could not fetch enough torrents!")
    except Exception as ef:
        await m.edit_text(ef)
    return
