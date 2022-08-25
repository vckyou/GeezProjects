# Copyright (C) 2020 Adek Maulana.
# All rights reserved.
# Port By @VckyouuBitch
# From Geez - Projects <https://github.com/vckyou/Geez-geezproject>
"""
   Heroku manager for your geezproject
"""

import math
import os

import aiohttp
import heroku3
import urllib3

from geezproject import BOTLOG_CHATID
from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME, SUDO_USERS
from geezproject.modules.sql_helper.globals import addgvar, delgvar, gvarstatus
from geezproject.utils import edit_or_reply, geez_cmd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


"""
   ConfigVars setting, get current var, set var or delete var...
"""


@geez_cmd(pattern="(get|del) var(?: |$)(\w*)")
async def variable(var):
    exe = var.pattern_match.group(1)
    if app is None:
        await edit_or_reply(
            var, "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **di Heroku**"
        )
        return False
    if var.sender_id in SUDO_USERS:
        return
    if exe == "get":
        xx = await edit_or_reply(var, "`Mendapatkan Informasi...`")
        variable = var.pattern_match.group(2)
        if variable == "":
            configvars = heroku_var.to_dict()
            if BOTLOG_CHATID:
                msg = "".join(
                    f"`{item}` = `{configvars[item]}`\n" for item in configvars
                )
                await var.client.send_message(
                    BOTLOG_CHATID, "#CONFIGVARS\n\n" "**Config Vars**:\n" f"{msg}"
                )
                await xx.edit("**Berhasil Mengirim Ke BOTLOG_CHATID**")
                return True
            await xx.edit("**Mohon Ubah Var** `BOTLOG` **Ke** `True`")
            return False
        if variable in heroku_var:
            if BOTLOG_CHATID:
                await var.client.send_message(
                    BOTLOG_CHATID,
                    "**Logger : #SYSTEM**\n\n"
                    "**#SET #VAR_HEROKU #ADDED**\n\n"
                    f"`{variable}` **=** `{heroku_var[variable]}`\n",
                )
                await xx.edit("**Berhasil Mengirim Ke BOTLOG_CHATID**")
                return True
            await xx.edit("**Mohon Ubah Var** `BOTLOG` **Ke** `True`")
            return False
        await var.edit("`Informasi Tidak Ditemukan...`")
        return True
    if exe == "del":
        xx = await edit_or_reply(var, "`Menghapus Config Vars...`")
        variable = var.pattern_match.group(2)
        if variable == "":
            await xx.edit("**Mohon Tentukan Config Vars Yang Mau Anda Hapus**")
            return False
        if variable in heroku_var:
            if BOTLOG_CHATID:
                await var.client.send_message(
                    BOTLOG_CHATID,
                    "**Logger : #SYSTEM**\n\n"
                    "**#SET #VAR_HEROKU #DELETED**\n\n"
                    f"`{variable}`",
                )
            await xx.edit("**Config Vars Telah Dihapus**")
            del heroku_var[variable]
        else:
            await xx.edit("**Tidak Dapat Menemukan Config Vars**")
            return True


@geez_cmd(pattern="set var (\w*) ([\s\S]*)")
async def set_var(var):
    if app is None:
        return await edit_or_reply(
            var, "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **dan** `HEROKU_API_KEY`"
        )
    if var.sender_id in SUDO_USERS:
        return
    xx = await edit_or_reply(var, "`Processing...`")
    variable = var.pattern_match.group(1)
    value = var.pattern_match.group(2)
    if variable in heroku_var:
        if BOTLOG_CHATID:
            await var.client.send_message(
                BOTLOG_CHATID,
                "**Logger : #SYSTEM**\n\n"
                "**#SET #VAR_HEROKU #ADDED**\n\n"
                f"`{variable}` = `{value}`",
            )
        await xx.edit("`Sedang Proses, Mohon Tunggu sebentar..`")
    else:
        if BOTLOG_CHATID:
            await var.client.send_message(
                BOTLOG_CHATID,
                "**Logger : #SYSTEM**\n\n"
                "**#SET #VAR_HEROKU #ADDED**\n\n"
                f"`{variable}` **=** `{value}`",
            )
        await xx.edit("**Berhasil Menambahkan Config Var**")
    heroku_var[variable] = value


"""
    Check account quota, remaining quota, used quota, used app quota
"""


@geez_cmd(pattern="(usage|kuota|dyno)(?: |$)")
async def dyno_usage(dyno):
    if app is None:
        return await dyno.edit(
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **dan** `HEROKU_API_KEY`"
        )
    xx = await edit_or_reply(dyno, "`Processing...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/81.0.4044.117 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    async with aiohttp.ClientSession() as session, session.get(
        heroku_api + path, headers=headers
    ) as r:
        if r.status != 200:
            await dyno.client.send_message(
                dyno.chat_id, f"`{r.reason}`", reply_to=dyno.id
            )
            await xx.edit("**Gagal Mendapatkan Informasi Dyno**")
            return False
        result = await r.json()
        quota = result["account_quota"]
        quota_used = result["quota_used"]

        """ - User Quota Limit and Used - """
        remaining_quota = quota - quota_used
        percentage = math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)
        day = math.floor(hours / 24)

        """ - User App Used Quota - """
        Apps = result["apps"]
        for apps in Apps:
            if apps.get("app_uuid") == app.id:
                AppQuotaUsed = apps.get("quota_used") / 60
                AppPercentage = math.floor(apps.get("quota_used") * 100 / quota)
                break
        else:
            AppQuotaUsed = 0
            AppPercentage = 0

        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)

        await xx.edit(
            "**Informasi Dyno Heroku :** \n"
            "╭┈─╼━━━━━━━━━━━━━╾─┈  \n"
            "│          ⚡Geez - Project⚡  \n"
            "├┈─╼━━━━━━━━━━━━━╾─┈  \n"
            "│💠 ᴘᴇɴɢɢᴜɴᴀᴀɴ ᴅʏɴᴏ ꜱᴀᴀᴛ ɪɴɪ \n"
            f"│  ▸ {AppHours} ᴊᴀᴍ - {AppMinutes} ᴍᴇɴɪᴛ. \n"
            f"│  ▸ ᴘʀᴇꜱᴇɴᴛᴀꜱᴇ : {AppPercentage}% \n"
            "├┈──────────────┈\n"
            "│💠 ᴘᴇɴɢɢᴜɴᴀᴀɴ ᴅʏɴᴏ ʙᴜʟᴀɴ ɪɴɪ \n"
            f"│  ▸ {hours} ᴊᴀᴍ - {minutes} ᴍᴇɴɪᴛ. \n"
            f"│  ▸ ᴘʀᴇꜱᴇɴᴛᴀꜱᴇ : {percentage}%. \n"
             "╰┈─────────────┈ \n"
            f"▸ **Sisa Dyno Anda** `{day}` **Hari Lagi**"
        )
        return True


@geez_cmd(pattern="logs")
async def _(dyno):
    if app is None:
        return await edit_or_reply(
            dyno, "**Wajib Mengisi Var** `HEROKU_APP_NAME` **dan** `HEROKU_API_KEY`"
        )
    xx = await edit_or_reply(dyno, "**Sedang Mengambil Logs Heroku**")
    data = app.get_log()
    await edit_or_reply(xx, data, deflink=True, linktext="**✣ Ini Logs Heroku Anda :**")


@geez_cmd(pattern="getdb ?(.*)")
async def getsql(event):
    if event.sender_id in SUDO_USERS:
        return
    var_ = event.pattern_match.group(1)
    xxnx = await edit_or_reply(event, f"**Getting variable** `{var_}`")
    if var_ == "":
        return await xxnx.edit(
            f"**Invalid Syntax !!** \n\nKetik `{cmd}getdb NAMA_VARIABLE`"
        )
    try:
        sql_v = gvarstatus(var_)
        os_v = os.environ.get(var_) or "None"
    except Exception as e:
        return await xxnx.edit(f"**ERROR !!**\n\n`{e}`")
    await xxnx.edit(
        f"**OS VARIABLE:** `{var_}`\n**OS VALUE :** `{os_v}`\n------------------\n**SQL VARIABLE:** `{var_}`\n**SQL VALUE :** `{sql_v}`\n"
    )


@geez_cmd(pattern="setdb ?(.*)")
async def setsql(event):
    if event.sender_id in SUDO_USERS:
        return
    hel_ = event.pattern_match.group(1)
    var_ = hel_.split(" ")[0]
    val_ = hel_.split(" ")[1:]
    valu = " ".join(val_)
    xxnx = await edit_or_reply(event, f"**Setting variable** `{var_}` **as** `{valu}`")
    if "" in (var_, valu):
        return await xxnx.edit(
            f"**Invalid Syntax !!**\n\n**Ketik** `{cmd}setsql VARIABLE_NAME value`"
        )
    try:
        addgvar(var_, valu)
    except Exception as e:
        return await xxnx.edit(f"**ERROR !!** \n\n`{e}`")
    await xxnx.edit(f"**Variable** `{var_}` **successfully added with value** `{valu}`")


@geez_cmd(pattern="deldb ?(.*)")
async def delsql(event):
    if event.sender_id in SUDO_USERS:
        return
    var_ = event.pattern_match.group(1)
    xxnx = await edit_or_reply(event, f"**Deleting Variable** `{var_}`")
    if var_ == "":
        return await xxnx.edit(
            f"**Invalid Syntax !!**\n\n**Ketik** `{cmd}delsql VARIABLE_NAME`"
        )
    try:
        delgvar(var_)
    except Exception as e:
        return await xxnx.edit(f"**ERROR !!**\n\n`{e}`")
    await xxnx.edit(f"**Deleted Variable** `{var_}`")


CMD_HELP.update(
    {
        "heroku": f"**Plugin : **`heroku`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}set var <nama var> <value>`\
        \n  ❍▸ : **Tambahkan Variabel Baru Atau Memperbarui Variabel Setelah Menyetel Variabel GeezProjects Akan Di Restart.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}get var or .get var <nama var>`\
        \n  ❍▸ : **Dapatkan Variabel Yang Ada,Harap Gunakan Di Grup Private Anda!\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}del var <nama var>`\
        \n  ❍▸ : **Untuk Menghapus var heroku\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}usage` atau `{cmd}kuota`\
        \n  ❍▸ : **Check Kouta Dyno Heroku\
    "
    }
)


CMD_HELP.update(
    {
        "database": f"**Plugin : **`database`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}setdb <nama var> <value>`\
        \n  ❍▸ : **Tambahkan Variabel SQL Tanpa Merestart geezproject.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}getdb <nama var>`\
        \n  ❍▸ : **Dapatkan Variabel SQL Yang Ada Harap Gunakan Di Grup Private Anda!\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}deldb <nama var>`\
        \n  ❍▸ : **Untuk Menghapus Variabel SQL\
    "
    }
)
