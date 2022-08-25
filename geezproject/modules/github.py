# Copyright (C) 2021 Catuserbot <https://github.com/sandy1709/catuserbot>
# Ported by @mrismanaziz
# recode by @vckyaz
# FROM GeezProjects <https://github.com/vckyou/GeezProjects>
#
# Support @GeezSupport & @GeezProjects

import os

import aiohttp
import requests
from pySmartDL import SmartDL

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, bot
from geezproject.events import geez_cmd
from geezproject.utils import edit_delete, edit_or_reply, reply_id

ppath = os.path.join(os.getcwd(), "temp", "githubuser.jpg")


@bot.on(geez_cmd(outgoing=True, pattern=r"github( -l(\d+))? ([\s\S]*)"))
async def _(event):
    "Get info about an GitHub User"
    reply_to = await reply_id(event)
    username = event.pattern_match.group(3)
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session, session.get(URL) as request:
        if request.status == 404:
            return await edit_delete(event, "`" + username + " Not Found`")
        catevent = await edit_or_reply(event, "`fetching github info ...`")
        result = await request.json()
        photo = result["avatar_url"]
        if result["bio"]:
            result["bio"] = result["bio"].strip()
        repos = []
        sec_res = requests.get(result["repos_url"])
        if sec_res.status_code == 200:
            limit = event.pattern_match.group(2)
            limit = 5 if not limit else int(limit)
            for repo in sec_res.json():
                repos.append(f"[{repo['name']}]({repo['html_url']})")
                limit -= 1
                if limit == 0:
                    break
        REPLY = "**GitHub Info for** `{username}`\
                \n👤 **Name :** [{name}]({html_url})\
                \n🔧 **Type :** `{type}`\
                \n🏢 **Company :** `{company}`\
                \n🔭 **Blog :** {blog}\
                \n📍 **Location :** `{location}`\
                \n📝 **Bio :** __{bio}__\
                \n❤️ **Followers :** `{followers}`\
                \n👁 **Following :** `{following}`\
                \n📊 **Public Repos :** `{public_repos}`\
                \n📄 **Public Gists :** `{public_gists}`\
                \n🔗 **Profile Created :** `{created_at}`\
                \n✏️ **Profile Updated :** `{updated_at}`".format(
            username=username, **result
        )

        if repos:
            REPLY += "\n🔍 **Some Repos** : " + " | ".join(repos)
        downloader = SmartDL(photo, ppath, progress_bar=False)
        downloader.start(blocking=False)
        await event.client.send_file(
            event.chat_id,
            ppath,
            caption=REPLY,
            reply_to=reply_to,
        )
        os.remove(ppath)
        await catevent.delete()


CMD_HELP.update(
    {
        "github": f"**Plugin : **`github`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}github` <username>\
        \n  ❍▸ : **Menampilkan informasi tentang user di GitHub dari username yang diberikan\
    "
    }
)
