import asyncio
from pyrogram import Client


try:
    from telepyrobot import APP_ID, API_HASH
except ModuleNotFoundError:
    APP_ID = int(input("Enter Telegram APP ID: "))
    API_HASH = input("Enter Telegram API HASH: ")


async def main(api_id, api_hash):
    """ Generate String Session for the current Memory Session"""
    async with Client(":memory:", api_id=api_id, api_hash=api_hash) as app:
        print(await app.export_session_string())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(APP_ID, API_HASH))
