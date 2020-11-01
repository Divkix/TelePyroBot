import aiohttp
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
import os

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Get information about a Github Account

**Usage:**
`{COMMAND_HAND_LER}github <github username>`
"""


@TelePyroBot.on_message(filters.command("github", COMMAND_HAND_LER) & filters.me)
async def github(c: TelePyroBot, m: Message):
    if len(m.text.split()) == 2:
        username = m.text.split(None, 1)[1]
    else:
        await m.edit_text(
            f"Usage: `{COMMAND_HAND_LER}github <username>`", parse_mode="md"
        )
        return

    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await m.edit_text(f"`{username} not found`", parse_mode="md")
                return

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = (
                f"**GitHub Info for** `{username}`"
                f"\n**Username:** `{name}`\n**Bio:** `{bio}`\n**URL:** {url}"
                f"\n**Company:** `{company}`\n**Created at:** `{created_at}`"
            )

            if not result.get("repos_url", None):
                return await m.edit_text(REPLY, parse_mode="md")
            async with session.get(result.get("repos_url", None)) as request:
                result = request.json
                if request.status == 404:
                    return await m.edit_text(REPLY, parse_mode="md")

                result = await request.json()

                REPLY += "\nRepos:\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await m.edit_text(REPLY, parse_mode="md")
    return
