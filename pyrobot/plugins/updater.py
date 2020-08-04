import asyncio
import os
import git
import os
from pyrogram import Client, Filters

from pyrobot import (
    COMMAND_HAND_LER,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    LOGGER,
    MAX_MESSAGE_LENGTH,
    OFFICIAL_UPSTREAM_REPO,
    OFFICIAL_BRANCH)

from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError, NoSuchPathError

# -- Constants -- #
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used \n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater.")
REPO_REMOTE_NAME = "tmp_upstream_remote"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
UPDATE_IN_PROGRESS = f"**Updating Application!** __Please wait upto 5 minutes....__\n\nDo `{COMMAND_HAND_LER}alive` or `{COMMAND_HAND_LER}start` to check if I'm alive"
# -- Constants End -- #

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Update your username to latest version!

`{COMMAND_HAND_LER}update`: Update userbot to latest version.
"""

async def gen_chlog(repo, diff):
    changelog = ""
    d_form = "%H:%M - %d/%m/%y"
    for cl in repo.iter_commits(diff):
        changelog += f'• [{cl.committed_datetime.strftime(d_form)}]: {cl.summary} <{cl.author}>\n'
    return changelog


@Client.on_message(Filters.command("update", COMMAND_HAND_LER) & Filters.me)
async def updater(client, message):
    await message.edit("`Checking for updating...`")
    try:
        repo = git.Repo()
    except git.exc.InvalidGitRepositoryError as error_one:
        LOGGER.info(str(error_one))
        repo = git.Repo.init()
        origin = repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(IFFUCI_ACTIVE_BRANCH_NAME, origin.refs.master)
        repo.heads.master.checkout(True)

    active_branch_name = repo.active_branch.name
    if active_branch_name not in OFFICIAL_BRANCH:
        await message.edit(f'**[UPDATER]:** Looks like you are using your own custom branch ({active_branch_name}). in that case, Updater is unable to identify which branch is to be merged. please checkout to any official branch')
        return

    LOGGER.info(active_branch_name)
    if active_branch_name != IFFUCI_ACTIVE_BRANCH_NAME:
        await message.edit(IS_SELECTED_DIFFERENT_BRANCH.format(
            branch_name=active_branch_name
        ))
        return False

    try:
        repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
    except Exception as error_two:
        LOGGER.info(str(error_two))

    tmp_upstream_remote = repo.remote(REPO_REMOTE_NAME)
    tmp_upstream_remote.fetch(active_branch_name)
    try:
        changelog = await gen_chlog(repo, HEROKU_GIT_REF_SPEC)
        changelog_file = "pyrobot/cache/changelog.txt"
        with open(changelog_file, "w", encoding="utf-8") as f:
            f.write(str(changelog))
            f.close()
        await message.reply_document(document=changelog_file,
                               caption="Here is the chat list that you joined.")
        os.remove(changelog_file)
    except Exception as err:
        if "fatal: bad revision" in str(err):
            await message.edit("`Cannot send Changelog`")
            pass

    await asyncio.sleep(5)
    await message.edit(UPDATE_IN_PROGRESS)
    repo.git.reset("--hard", "FETCH_HEAD")

    if HEROKU_API_KEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = heroku.apps()[HEROKU_APP_NAME]
        heroku_git_url = heroku_app.git_url.replace(
            "https://",
            "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        remote.push(refspec=HEROKU_GIT_REF_SPEC, force=True)
    else:
        await message.edit(NO_HEROKU_APP_CFGD)