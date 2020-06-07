from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.cust_p_filters import sudo_filter

class Custom(dict):
    def __missing__(self, key):
        return 0


@Client.on_message(Filters.command("metrics", COMMAND_HAND_LER) & sudo_filter)
async def get_id(client, message):
    await message.delete()
    words = Custom()
    progress = await client.send_message(message.chat.id, "`Processed 0 messages...`", parse_mode="md")
    total = 0
    async for msg in client.iter_history(message.chat.id, 1000):
        total += 1
        if total % 100 == 0:
            await progress.edit_text(f"`Processed {total} messages...`", parse_mode="md")
            time.sleep(0.5)
        if msg.text:
            for word in msg.text.split():
                words[word.lower()] += 1
        if msg.caption:
            for word in msg.caption.split():
                words[word.lower()] += 1
    freq = sorted(words, key=words.get, reverse=True)
    out = "Word Counter\n"
    for i in range(25):
        out += f"{i + 1}. **{words[freq[i]]}**: {freq[i]}\n"
    await progress.edit_text(out, parse_mode="md")
