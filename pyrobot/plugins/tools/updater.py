"""Update User / Bot code
Syntax: .update"""

import asyncio
import os
import git

from pyrogram import Client, Filters

from pyrobot import (
    COMMAND_HAND_LER,
    HEROKU_API_KEY,
    LOGGER,
    MAX_MESSAGE_LENGTH,
    OFFICIAL_UPSTREAM_REPO
)

from pyrobot.helper_functions.cust_p_filters import owner_filter

# -- Constants -- #
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used \n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)
BOT_IS_UP_TO_DATE = "the user / bot is up-to-date."
NEW_BOT_UP_DATE_FOUND = (
    "new update found for {branch_name}\n"
    "chagelog: \n\n{changelog}\n"
    "updating ..."
)
NEW_UP_DATE_FOUND = (
    "new update found for {branch_name}\n"
    "updating ..."
)
REPO_REMOTE_NAME = "tmp_upstream_remote"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
DIFF_MARKER = "HEAD..{remote_name}/{branch_name}"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku application"
# -- Constants End -- #


@Client.on_message(Filters.command("update", COMMAND_HAND_LER) & owner_filter)
async def updater(client, message):
    status_message = await message.reply_text("__Checking for update....__", parse_mode="md")
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
        await status_message.edit(IS_SELECTED_DIFFERENT_BRANCH.format(
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

    updatenochange = await status_message.edit("`Updating Please Wait...`", parse_mode="md")
    await asyncio.sleep(8)

    tmp_upstream_remote.fetch(active_branch_name)
    repo.git.reset("--hard", "FETCH_HEAD")

    if HEROKU_API_KEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            heroku_app = heroku_applications[0]
            heroku_git_url = heroku_app.git_url.replace(
                "https://",
                "https://api:" + HEROKU_API_KEY + "@"
            )
            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(heroku_git_url)
            else:
                remote = repo.create_remote("heroku", heroku_git_url)
            remote.push(refspec=HEROKU_GIT_REF_SPEC)
        else:
            await message.reply(NO_HEROKU_APP_CFGD)

    await status_message.edit(RESTARTING_APP)
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
    await updatenochange.edit("**Updated!**\nPLease wait upto 5 minutes to let the session start!\n\n "
        f"Do `{COMMAND_HAND_LER}alive` or `{COMMAND_HAND_LER}start` to check if I am online?", parse_mode="md")
