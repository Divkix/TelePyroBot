import io
import os
import sys
import traceback
import time
import asyncio
import requests
from pyrogram import Client, Filters
from pyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Evaluate Python Code inside Telegram
Syntax: `{COMMAND_HAND_LER}eval PythonCode`

Run command on file system from Telegram
Syntax: `{COMMAND_HAND_LER}exec CommandCode`

Get IP Address of userbot server.
Syntax: `{COMMAND_HAND_LER}ip`
"""


@Client.on_message(Filters.command("eval", COMMAND_HAND_LER) & Filters.me)
async def eval(client, message):
    status_message = await message.reply_text("`Processing...`")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
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

    final_output = "<b>EVAL</b>: <code>{}</code>\n\n<b>OUTPUT</b>:\n<code>{}</code> \n".format(
        cmd,
        evaluation.strip()
    )

    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("eval.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document="eval.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("eval.text")
        await status_message.delete()
    else:
        await status_message.edit(final_output)


async def aexec(code, client, message):
    exec(
        f'async def __aexec(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](client, message)


@Client.on_message(Filters.command("exec", COMMAND_HAND_LER) & Filters.me)
async def execution(_, message):
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id

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
        await message.reply_document(
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("exec.text")
    else:
        await message.reply_text(OUTPUT)


@Client.on_message(Filters.command("ip", COMMAND_HAND_LER) & Filters.me)
async def public_ip(client, message):
    ip = requests.get('https://api.ipify.org').text
    await message.edit(f'<b>Bot IP Address:</b>\n\n<code>{ip}</code>', parse_mode='html')
