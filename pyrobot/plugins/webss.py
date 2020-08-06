import asyncio
from re import match

import aiofiles
from selenium import webdriver

import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, GOOGLE_CHROME_BIN, TMP_DOWNLOAD_DIRECTORY

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Get screenshot of website using selenium easily using userbot!

`{COMMAND_HAND_LER}webss <url>`
"""

@Client.on_message(Filters.command("webss", COMMAND_HAND_LER) & Filters.me)
async def weather(client, message):
    if GOOGLE_CHROME_BIN is None:
        await message.edit("You need to install Google Chrome. Module Stopping!!")
        return
    link_match = match(r'\bhttps?://.*\.\S+', message.text.split(" ",1)[1])
    if not link_match:
        await message.edit("`I need a valid link to take screenshots from.`")
        return
    link = link_match.group()
    await message.edit("`Processing ...`")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(link)
    height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);")
    width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
        "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
        "document.documentElement.offsetWidth);")
    driver.set_window_size(width + 125, height + 125)
    wait_for = height / 1000
    await message.edit(f"`Generating screenshot of the page...`"
                       f"\n`Height of page = {height}px`"
                       f"\n`Width of page = {width}px`"
                       f"\n`Waiting ({int(wait_for)}s) for the page to load.`")
    await asyncio.sleep(int(wait_for))
    im_png = driver.get_screenshot_as_png()
    driver.close()
    message_id = message.message_id
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
    file_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, "webss.png")
    async with aiofiles.open(file_path, 'wb') as out_file:
        await out_file.write(im_png)
    await asyncio.gather(
        message.delete(),
        client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            caption=f"**Link:** {link}\nWeb SS taken using @TelePyroBot",
            reply_to_message_id=message_id)
    )
    os.remove(file_path)
    driver.quit()
    return
