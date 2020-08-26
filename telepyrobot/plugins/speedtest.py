from pyrogram import Client, filters
from telepyrobot import COMMAND_HAND_LER
from speedtest import Speedtest
import os

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}speedtest`: Get speedtest of your server.
"""


@Client.on_message(filters.command("speedtest", COMMAND_HAND_LER) & filters.me)
async def listbots(client, message):
    await message.edit("`Running speed test . . .`")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    await message.edit(
        "**Started at:** "
        f"`{result['timestamp']}`\n\n"
        "**Download:** "
        f"`{speed_convert(result['download'])}`\n"
        "**Upload:** "
        f"`{speed_convert(result['upload'])}`\n"
        "**Ping:** "
        f"`{result['ping']} ms`\n"
        "**ISP:** "
        f"`{result['client']['isp']}`",
        parse_mode="markdown",
    )


def speed_convert(size):
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"
