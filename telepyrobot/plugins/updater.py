import asyncio
import os
import git
import shutil
import heroku3
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot.utils.cust_p_filters import sudo_filter
from telepyrobot import (
    COMMAND_HAND_LER,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    LOGGER,
    MAX_MESSAGE_LENGTH,
    OFFICIAL_UPSTREAM_REPO,
    PRIVATE_GROUP_ID,
)

# -- Constants -- #
IS_SELECTED_DIFFERENT_BRANCH = (
    "Looks like a custom branch {branch_name} "
    "is being used\n"
    "In this case, updater is unable to identify the branch to be updated."
    "Please check out to an official branch, and re-start the updater.\n\n"
    "Or join @TelePyroBot for help!"
)
REPO_REMOTE_NAME = "official_remote"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
DIFF_MARKER = "HEAD..{remote_name}/{branch_name}"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
NEW_BOT_UP_DATE_FOUND = "**NEW update found for** __{branch_name}__( {commit_link})\n**Chagelog:**\n\n`{changelog}`\n__**Updating...**__"
NEW_UP_DATE_FOUND = "**NEW Update found for** __{branch_name}__\n__**Updating ...**__"
# -- Constants End -- #

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
**Update your Userbot easily ✌️**

`{COMMAND_HAND_LER}update`: Update userbot to latest version.
`{COMMAND_HAND_LER}update force`: Forcefully update userbot to sync with latest remote source!
"""


@TelePyroBot.on_message(filters.command("update", COMMAND_HAND_LER) & sudo_filter)
async def updater(c: TelePyroBot, m: Message):
    if len(m.command) == 2 and m.command[1] == "force":
        force_update = True
    else:
        force_update = False

    umsg = await m.reply_text("`Checking for Update...`")
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        await umsg.edit(
            "__Please the Vars__ `HEROKU_API_KEY` __and__ `HEROKU_APP_NAME` __properly!__"
        )
        return
    if PRIVATE_GROUP_ID is None:
        await umsg.edit("__**Please Set**__ `PRIVATE_GROUP_ID` **__to use updater!__**")
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
        await umsg.edit(
            IS_SELECTED_DIFFERENT_BRANCH.format(
                branch_name=active_branch_name, COMMAND_HAND_LER=COMMAND_HAND_LER
            )
        )
        return

    try:
        repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
    except Exception as error_two:
        LOGGER.info(str(error_two))

    temp_remote = repo.remote(REPO_REMOTE_NAME)
    temp_remote.fetch(active_branch_name)

    changelog = generate_change_log(
        repo,
        DIFF_MARKER.format(
            remote_name=REPO_REMOTE_NAME, branch_name=active_branch_name
        ),
    )
    LOGGER.info(changelog)

    try:
        remote_head_github = repo.head.reference
        commit_id = remote_head_github.commit.hexsha
        commit_link = f"<a href='https://github.com/SkuzzyxD/TelePyroBot/commit/{commit_id}'>{commit_id[:7]}</a>"
    except:
        commit_link = "None"

    message_one = NEW_BOT_UP_DATE_FOUND.format(
        branch_name=active_branch_name, changelog=changelog, commit_link=commit_link
    )
    message_two = NEW_UP_DATE_FOUND.format(branch_name=active_branch_name)

    if len(message_one) > MAX_MESSAGE_LENGTH:
        with open("change.log", "w+", encoding="utf8") as out_file:
            out_file.write(str(message_one))
        await m.reply_document(
            document="change.log",
            caption=message_two,
            disable_notification=True,
            reply_to_message_id=m.message_id,
        )
        os.remove("change.log")

    if not changelog and force_update == False:
        await umsg.edit("`Your userbot is already up-to-date!!`")
        return

    await umsg.edit(message_one, disable_web_page_preview=True)

    if force_update == True:
        await umsg.edit(
            "**Force-Update initiated**\n`Fetching latest version and installing it...`"
        )
        changelog = "#ForceUpdate"

    temp_remote.fetch(active_branch_name)
    repo.git.reset("--hard", "FETCH_HEAD")

    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_app = heroku.apps()[HEROKU_APP_NAME]
    heroku_git_url = heroku_app.git_url.replace(
        "https://", f"https://api:{HEROKU_API_KEY}@"
    )
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    await umsg.reply(
        f"**Update Started**\n__**Type**__ `{COMMAND_HAND_LER}alive` **__to check if I'm alive__**\n\n**It would take upto 5 minutes to update!**"
    )
    await c.send_message(
        PRIVATE_GROUP_ID,
        f"#UPDATE\n\n**__TelePyroBot Update__** {commit_link}\n\n**Changelog:**\n{changelog}",
        disable_web_page_preview=True,
    )
    remote.push(refspec=HEROKU_GIT_REF_SPEC, force=True)
    asyncio.get_event_loop().create_task(deploy_start(client))


def generate_change_log(git_repo, diff_marker):
    changelog_string = ""
    d_form = "%d/%m/%y"
    for repo_change in git_repo.iter_commits(diff_marker):
        changelog_string += f"•[{repo_change.committed_datetime.strftime(d_form)}]: {repo_change.summary} ({repo_change.author})\n"
    return changelog_string


async def deploy_start(client):
    await c.restart()
