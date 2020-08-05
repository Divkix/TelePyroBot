import asyncio
import os
from pyrogram import Client, Filters
import git
from git import Repo
from git.exc import GitCommandError
from pyrobot import (
    COMMAND_HAND_LER,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    LOGGER,
    MAX_MESSAGE_LENGTH,
    OFFICIAL_UPSTREAM_REPO,
    PRIVATE_GROUP_ID)

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
**Update your Userbot easily ✌️**

`{COMMAND_HAND_LER}update`: Update userbot to latest version.
`{COMMAND_HAND_LER}reinstall`: Reinstall the userbot from  Official Github Repo.
"""

@Client.on_message(Filters.command("update", COMMAND_HAND_LER) & Filters.me)
async def updater(client, message):
    await message.edit("`Checking for Update...`")
    repo = Repo()
    ups_rem = repo.remote(OFFICIAL_UPSTREAM_REPO)

    try:
        ups_rem.fetch()
    except GitCommandError as error:
        await message.edit(f"**Error:**\n`{error}`")
        return

    for ref in ups_rem.refs:
        branch = str(ref).split('/')[-1]
        if branch not in repo.branches:
            repo.create_head(branch, ref)

    branch = "master"
    if len(message.text.split(" ")) >= 2:
        branch = message.text.split(" ",1)[1]
    if branch not in repo.branches:
        await message.edit(f'**Invalid branch name:** {branch}')
        return
    out = ''
    try:
        for i in repo.iter_commits(f'HEAD..{Config.UPSTREAM_REMOTE}/{branch}'):
            out += (f"🔨 **#{i.count()}** : "
                    f"[{i.summary}]({Config.UPSTREAM_REPO.rstrip('/')}/commit/{i}) "
                    f"👷 __{i.committer}__\n\n")
    except GitCommandError as error:
        await message.edit(f"**Error:**\n`{error}`")
        return

    if out:
        await message.edit(f'`New update found for [{branch}], Now pulling...`')
        await asyncio.sleep(1)
        repo.git.reset('--hard', 'FETCH_HEAD')
        await client.send_message(PRIVATE_GROUP_ID,
            f"**UPDATED TelePyroBot from [{branch}]:\n\n📄 CHANGELOG 📄**\n\n{out}")
    else:
        await message.edit("**__TelePyroBot is upto date!__**")

    if (HEROKU_API_KEY or HEROKU_APP_NAME) is not None:
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
        remote.push(refspec=f'{branch}:master', force=True)
    else:
        await message.edit(NO_HEROKU_APP_CFGD)
