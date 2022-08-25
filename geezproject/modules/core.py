# ported by @mrismanaziz
# recode by @vckyaz
# FROM GeezProjects <https://github.com/vckyou/GeezProjects>
#
# Support @GeezSupport & @GeezProjects

import os
from pathlib import Path

from geezproject import CMD_HELP, bot
from geezproject.events import geez_cmd
from geezproject.utils import edit_or_reply, load_module, remove_plugin, reply_id


@bot.on(geez_cmd(outgoing=True, pattern="install$"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            await event.edit("`Installing Modules...`")
            downloaded_file_name = (
                await event.client.download_media(  # pylint:disable=E0602
                    await event.get_reply_message(),
                    "geezproject/modules/",  # pylint:disable=E0602
                )
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit(
                    "**Plugin** `{}` **Berhasil di install**".format(
                        os.path.basename(downloaded_file_name)
                    )
                )
            else:
                os.remove(downloaded_file_name)
                await event.edit("**Error!** Plugin ini sudah terinstall di geezproject.")
        except Exception as e:
            await event.edit(str(e))
            os.remove(downloaded_file_name)


@bot.on(geez_cmd(outgoing=True, pattern=r"psend ([\s\S]*)"))
async def send(event):
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    the_plugin_file = f"./geezproject/modules/{input_str}.py"
    if os.path.exists(the_plugin_file):
        caat = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            thumb="geezproject/resources/logo.jpg",
            allow_cache=False,
            reply_to=reply_to_id,
            caption=f"➠ **Nama Plugin:** `{input_str}`",
        )
        await event.delete()
    else:
        await edit_or_reply(event, "**ERROR: Modules Tidak ditemukan**")


@bot.on(geez_cmd(outgoing=True, pattern=r"uninstall (?P<shortname>\w+)"))
async def uninstall(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    dir_path = f"./geezproject/modules/{shortname}.py"
    try:
        remove_plugin(shortname)
        os.remove(dir_path)
        await event.edit(f"**Berhasil Menghapus Modules** `{shortname}`")
    except OSError as e:
        await event.edit("**ERROR:** `%s` : %s" % (dir_path, e.strerror))


CMD_HELP.update(
    {
        "core": "**Plugin : **`core`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.install` <reply ke file module>\
        \n  ❍▸ : **Untuk Menginstall module geezproject secara instan.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.uninstall` <nama module>\
        \n  ❍▸ : **Untuk Menguninstall / Menghapus module geezproject secara instan.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.psend` <nama module>\
        \n  ❍▸ : **Untuk Mengirim module geezproject secara instan.\
    "
    }
)
