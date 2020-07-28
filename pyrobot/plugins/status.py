import asyncio
import psutil
import platform
import shutil
# -- Pyrogram -- #
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.cust_p_filters import sudo_filter

# Helper Function
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


status_text = f"""
<b>System:</b> <code>{platform.uname().system}</code>
<b>Release:</b> <code>{platform.uname().release}</code>
<b>Version:</b> <code>{platform.uname().version}</code>
<b>Machine</b> <code>{platform.uname().machine}</code>
<b>Cores:</b> <code>{psutil.cpu_count(logical=False)}</code>

<b><u>RAM</u></b>
<b>Total:</b> <code>{get_size(psutil.virtual_memory().total)}</code>
<b>Used</b> <code>{get_size(psutil.virtual_memory().used)}</code> | <code>{psutil.virtual_memory().percent}%</code>
<b>Available:</b> <code>{get_size(psutil.virtual_memory().available)}</code>

<b><u>DISK</u></b>
<b>Total:</b> <code>{get_size(shutil.disk_usage(".")[0])}</code>
<b>Used:</b> <code>{get_size(shutil.disk_usage(".")[1])}</code> | <code>{round((shutil.disk_usage(".")[1])/(shutil.disk_usage(".")[0]), 2) * 100}%</code>
<b>Available:</b> <code>{get_size(shutil.disk_usage(".")[2])}</code>
"""

@Client.on_message(Filters.command("status", COMMAND_HAND_LER) & sudo_filter)
async def show_status(client, message):
    await message.edit(status_text)
    return