import requests
import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}short <long-link>`: Will return shortlink of the long-link.

`{COMMAND_HAND_LER}unshort <shortlink>`: Will return long url of the shortlink.
"""

@Client.on_message(Filters.command("short", COMMAND_HAND_LER) & Filters.me)
async def short_link(client, message):
    input_str = message.text.split(" ", 1)[1]
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await message.edit(f"**Generated Link:**\n {response_api} for {input_str}.")
    else:
        await message.edit("something is wrong. please try again later.")


@Client.on_message(Filters.command("unshort", COMMAND_HAND_LER) & Filters.me)
async def unshort_link(client, message):
    input_str = message.text.split(" ", 1)[1]
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith('3'):
        await message.edit(f"Input URL: {input_str}\nReDirected URL: {r.headers["Location"]}"
    else:
        await message.edit(f"Input URL {input_str} returned status_code {r.status_code}")
