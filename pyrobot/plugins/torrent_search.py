import requests
import json
import asyncio
import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ =  f"""
Get Screenshot of any website.

`{COMMAND_HAND_LER}tsearch <query>`: Search for torrent query and display results.
"""

@Client.on_message(Filters.command("tsearch", COMMAND_HAND_LER) & Filters.me)
async def tor_search(client, message):
    if len(message.command) == 1:
        await message.edit("`Check help on how to use this command`")
        return
    await message.edit("`Please wait, fetching results...`")
    query = message.text.split(" ", 1)[1]
    response = requests.get(f"https://sjprojectsapi.herokuapp.com/torrent/?query={query}")
    ts = json.loads(response.text)
    if not ts == response.json():
        await message.edit("**Some error occured**\n`Try Again Later`")
        return
    listdata = ""
    run = 0
    while True:
        try:
            run += 1
            r1 = ts[run]
            list1 = "<-----{}----->\nName: {}\nSeeders: {}\nSize: {}\nAge: {}\n<--Magnet Below-->\n{}\n\n\n".format(run, r1['name'], r1['seeder'], r1['size'], r1['age'], r1['magnet'])
            listdata = listdata + list1
        except:
            break

    tsfileloc = f"{TMP_DOWNLOAD_DIRECTORY}/torrent_search.txt"
    caption = f"Here are the results for the query: {query}"
    with open(tsfileloc, "w+", encoding="utf8") as out_file:
        out_file.write(str(listdata))
    await message.reply_document(
        document=tsfileloc,
        caption=caption,
        disable_notification=True)
    os.remove(tsfileloc)
    await message.delete()
