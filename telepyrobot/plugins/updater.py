import os
import shutil
import sys

from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError, NoSuchPathError
from pyrogram import filters

from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot.utils.cust_p_filters import sudo_filter
from telepyrobot import (
    COMMAND_HAND_LER,
    LOGGER,
    MAX_MESSAGE_LENGTH,
    OFFICIAL_UPSTREAM_REPO,
    PRIVATE_GROUP_ID,
)

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
**Update your Userbot easily ✌️**

`{COMMAND_HAND_LER}update`: Update userbot to latest version.
`{COMMAND_HAND_LER}update now`: Forcefully update userbot to sync with latest remote source!
"""


async def gen_chlog(repo, diff):
    changelog = ""
    d_form = "%H:%M - %d/%m/%y"
    for cl in repo.iter_commits(diff):
        changelog += f"• [{cl.committed_datetime.strftime(d_form)}]: {cl.summary} <{cl.author}>\n"
    return changelog


async def initial_git(repo):
    isexist = os.path.exists("telepyrobot-old")
    if isexist:
        shutil.rmtree("telepyrobot-old")
    os.mkdir("telepyrobot-old")
    os.rename("telepyrobot", "telepyrobot-old/telepyrobot")
    os.rename(".gitignore", "telepyrobot-old/.gitignore")
    os.rename("LICENSE.md", "telepyrobot-old/LICENSE.md")
    os.rename("README.md", "telepyrobot-old/README.md")
    os.rename("requirements.txt", "telepyrobot-old/requirements.txt")
    os.rename("string-requirements.txt", "telepyrobot-old/string-requirements.txt")
    os.rename("heroku.yml", "telepyrobot-old/heroku.yml")
    update = repo.create_remote("master", REPOSITORY)
    update.pull("master")
    os.rename("telepyrobot-old/telepyrobot/config.py", "telepyrobot/sample_config.py")
    shutil.rmtree("telepyrobot/session/")


@TelePyroBot.on_message(filters.command("update", COMMAND_HAND_LER) & sudo_filter)
async def updater(c: TelePyroBot, m: Message):
    initial = False
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await m.edit_text(
            f"**Update failed!**\n\nError:\n`directory {error} is not found`",
        )
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        initial = True
    except GitCommandError as error:
        await m.edit_text(f"**Update failed!**\n\nError:\n`{error}`")
        return

    if initial:
        if len(m.text.split()) != 2:
            await m.edit_text(
                "Your git workdir is missing!\nI need to repair it!\nJust do `update now` to repair and update!",
            )
            return
        elif len(m.text.split()) == 2 and m.text.split()[1] == "now":
            try:
                await initial_git(repo)
            except Exception as err:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                await m.edit_text(f"**Error:**\n{err}")
                await m.reply_text(
                    f"exc_type: `{exc_type}`\nexc_obj: `{exc_obj}`\nexc_tb:`{exc_tb}`"
                )
                return
            await m.edit_text("Successfully Updated!\nBot is restarting...")
            await m.send_message(
                PRIVATE_GROUP_ID,
                "-> **WARNING**: Bot has been created a new git and sync to latest version, your old files is in telepyrobot-old",
            )
            await restart_all()
            return

    brname = repo.active_branch.name
    if brname not in OFFICIAL_BRANCH:
        await m.edit_text(
            f"**[UPDATER]:** Looks like you are using your own custom branch ({brname}). in that case, Updater is unable to identify which branch is to be merged. please checkout to any official branch",
        )
        return
    try:
        repo.create_remote("upstream", REPOSITORY)
    except BaseException:
        pass

    upstream = repo.remote("upstream")
    upstream.fetch(brname)
    try:
        changelog = await gen_chlog(repo, f"HEAD..upstream/{brname}")
    except Exception as err:
        if "fatal: bad revision" in str(err):
            try:
                await initial_git(repo)
            except Exception as err:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                await m.edit_text(f"**Error:**\n{err}")
                await m.reply_text(
                    f"exc_type: `{exc_type}`\nexc_obj: `{exc_obj}`\nexc_tb:`{exc_tb}`"
                )
                return
            await m.edit_text("Successfully Updated!\nBot is restarting...")
            await m.reply_text(
                "-> **WARNING**: Bot has been created a new git and sync to latest version, your old files is in telepyrobot-old"
            )
            await restart_all()
            return
        exc_type, exc_obj, exc_tb = sys.exc_info()
        await m.reply_text("An error has accured!")
        await m.reply_text(
            f"exc_type: `{exc_type}`\nexc_obj: `{exc_obj}`\nexc_tb:`{exc_tb}`"
        )
        return

    if not changelog:
        await m.edit_text(f"TelePyroBot is up-to-date with branch **{brname}**\n")
        return

    if len(m.text.split()) != 2:
        changelog_str = (
            f"To update latest changelog, do\n-> `update now`\n\n**New UPDATE available for [{brname}]:\n"
            f"\nCHANGELOG:**\n`{changelog}` "
        )
        if len(changelog_str) > 4096:
            await m.reply_text("`Changelog is too big, view the file to see it.`")
            with open("telepyrobot/cache/output.txt", "w+") as file:
                file.write(changelog_str)
            await client.send_document(
                m.chat.id,
                "telepyrobot/cache/output.txt",
                reply_to_message_id=m.message_id,
                caption="`Changelog file`",
            )
            os.remove("telepyrobot/cache/output.txt")
        else:
            await m.reply_text(changelog_str)
        return
    elif len(m.text.split()) == 2 and m.text.split()[1] == "now":
        await m.reply_text("`New update found, updating...`")
        try:
            upstream.pull(brname)
            await m.reply_text("Successfully Updated!\nBot is restarting...")
        except GitCommandError:
            repo.git.reset("--hard")
            repo.git.clean("-fd", "telepyrobot/modules/")
            repo.git.clean("-fd", "telepyrobot/utils/")
            repo.git.clean("-fd", "telepyrobot/db/")
            await m.reply_text("Successfully Updated!\nBot is restarting...")
        await m.send_message(PRIVATE_GROUP_ID, changelog)
        await restart_all()
    else:
        await m.reply_text(
            "Usage:\n-> `update` to check update\n-> `update now` to update latest commits\nFor more information ",
        )
    return
