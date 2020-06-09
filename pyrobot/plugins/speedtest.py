from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from speedtest import Speedtest

__PLUGIN__ = "Speedtest"

__help__ = f"""
{COMMAND_HAND_LER}speedtest: Get speedtest of your server.
"""

@Client.on_message(Filters.command("speedtest", COMMAND_HAND_LER) & Filters.me)
async def listbots(client, message):
    try:
        rm = await message.edit("`Running speed test . . .`")
    except:
        rm = await message.reply_text("`Running speed test . . .`")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    await rm.edit("`"
                       "Started at "
                       f"{result['timestamp']} \n\n"
                       "Download "
                       f"{speed_convert(result['download'])} \n"
                       "Upload "
                       f"{speed_convert(result['upload'])} \n"
                       "Ping "
                       f"{result['ping']} \n"
                       "ISP "
                       f"{result['client']['isp']}"
                       "`", parse_mode="md")


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"
