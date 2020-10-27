import io
import os
import sys
import traceback
import time
import asyncio
import requests
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER
from telepyrobot.utils.cust_p_filters import sudo_filter

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Evaluate Python Code inside Telegram
**Syntax:** `{COMMAND_HAND_LER}py PythonCode`

Run command on file system from Telegram
**Syntax:** `{COMMAND_HAND_LER}sh CommandCode`

Get IP Address of userbot server.
**Syntax:** `{COMMAND_HAND_LER}ip`
"""


@TelePyroBot.on_message(filters.command(["eval", "py"], COMMAND_HAND_LER) & sudo_filter)
async def eval(c: TelePyroBot, m: Message):
    status_m = await m.reply_text("`Processing...`")
    cmd = m.text.split(" ", maxsplit=1)[1]

    reply_to_id = m.message_id
    if m.reply_to_message:
        reply_to_id = m.reply_to_message.message_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, c, m)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = (
        "<b>EVAL</b>: <code>{}</code>\n\n<b>OUTPUT</b>:\n<code>{}</code> \n".format(
            cmd, evaluation.strip()
        )
    )

    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("eval.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await m.reply_document(
            document="eval.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove("eval.text")
        await status_m.delete()
    else:
        await status_m.edit(final_output)
    return


async def aexec(code, c, m):
    exec(
        f"async def __aexec(c: TelePyroBot, m: Message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](c, m)


@TelePyroBot.on_message(filters.command(["exec", "sh"], COMMAND_HAND_LER) & sudo_filter)
async def execution(_, m:  Message):
    cmd = m.text.split(" ", maxsplit=1)[1]

    reply_to_id = m.message_id
    if m.reply_to_message:
        reply_to_id = m.reply_to_message.message_id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "No Output"

    OUTPUT = ""
    OUTPUT += f"<b>QUERY:</b>\n<u>Command:</u>\n<code>{cmd}</code> \n"
    OUTPUT += f"<u>PID</u>: <code>{process.pid}</code>\n\n"
    OUTPUT += f"<b>stderr</b>: \n<code>{e}</code>\n\n"
    OUTPUT += f"<b>stdout</b>: \n<code>{o}</code>"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await m.reply_document(
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove("exec.text")
    else:
        await m.reply_text(OUTPUT)
    return


@TelePyroBot.on_message(filters.command("ip", COMMAND_HAND_LER) & sudo_filter)
async def public_ip(c: TelePyroBot, m: Message):
    ip = requests.get("https://api.ipify.org").text
    await m.reply_text(f"<b>Bot IP Address:</b>\n<code>{ip}</code>", parse_mode="html")
    return
