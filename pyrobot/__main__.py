"""from pyrobot.pyrobot import PyroBot

if __name__ == "__main__":
    app = PyroBot()
    app.run()"""


#Remove afterwards.............
import asyncio
from pyrobot import app
loop = asyncio.get_event_loop()

async def start_bot():
    await app.start()

if __name__ == '__main__':
    loop.run_until_complete(start_bot())
#Remove afterwards.............
