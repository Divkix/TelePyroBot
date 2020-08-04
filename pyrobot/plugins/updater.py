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
    OFFICIAL_UPSTREAM_REPO)

# -- Constants -- #
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used \n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater.")
REPO_REMOTE_NAME = "tmp_upstream_remote"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
DIFF_MARKER = "HEAD..{remote_name}/{branch_name}"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
BOT_IS_UP_TO_DATE = "**__TelePyroBot is already upto date!__**"
NEW_BOT_UP_DATE_FOUND = "**NEW update found for** __{branch_name}__\n**Chagelog:**\n\n`{changelog}`\n__**Updating...**__"
NEW_UP_DATE_FOUND = "**NEW Update found for** __{branch_name}__\n__**Updating ...**__"
# -- Constants End -- #

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}update`: Update userbot to latest version.
"""

@Client.on_message(Filters.command("update", COMMAND_HAND_LER) & Filters.me)
async def updater(client, message):
    await message.edit("`Updating Please Wait...`")
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

    changelog = generate_change_log(
        repo,
        DIFF_MARKER.format(
            remote_name=REPO_REMOTE_NAME,
            branch_name=active_branch_name
        )
    )
    LOGGER.info(changelog)

    if not changelog:
        await message.edit(BOT_IS_UP_TO_DATE)
        return

    message_one = NEW_BOT_UP_DATE_FOUND.format(
        branch_name=active_branch_name,
        changelog=changelog
    )
    message_two = NEW_UP_DATE_FOUND.format(
        branch_name=active_branch_name
    )

    if len(message_one) > MAX_MESSAGE_LENGTH:
        with open("change.log", "w+", encoding="utf8") as out_file:
            out_file.write(str(message_one))
        await message.reply_document(
            document="change.log",
            caption=message_two,
            disable_notification=True,
            reply_to_message_id=message.message_id
        )
        os.remove("change.log")
    else:
        await message.reply(message_one)

    await asyncio.sleep(3)
    tmp_upstream_remote.fetch(active_branch_name)
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

    asyncio.get_event_loop().create_task(restart(client, status_message))


def generate_change_log(git_repo, diff_marker):
    out_put_str = ""
    d_form = "%d/%m/%y"
    for repo_change in git_repo.iter_commits(diff_marker):
        out_put_str += f"•[{repo_change.committed_datetime.strftime(d_form)}]: "
        out_put_str += f"{repo_change.summary} <{repo_change.author}>\n"
    return out_put_str


async def restart(client, message):
    await client.restart()
    await message.edit(
        "**Restarted!**\n"
        f"do `{COMMAND_HAND_LER}alive` to check if I am online :p"
    )