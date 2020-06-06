"""from pyrobot.pyrobot import PyroBot

if __name__ == "__main__":
    app = PyroBot()
    app.run()"""


#Remove afterwards.............
from pyrobot import app

async def start_bot():
    await app.start()

if __name__ == '__main__':
    app.run()
#Remove afterwards.............
