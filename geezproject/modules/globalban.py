import asyncio
from datetime import datetime
from io import BytesIO

from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import Channel

import geezproject.modules.sql_helper.gban_sql as gban_sql
from geezproject import BOTLOG_CHATID
from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, DEVS, bot
from geezproject.events import register
from geezproject.utils import edit_or_reply, geez_cmd, get_user_from_event

from .admin import BANNED_RIGHTS, UNBAN_RIGHTS


async def admin_groups(grp):
    admgroups = []
    async for dialog in grp.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            admgroups.append(entity.id)
    return admgroups


def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"


@geez_cmd(pattern="gban(?: |$)(.*)")
@register(pattern=r"^\.cgban(?: |$)(.*)", sudo=True)
async def gban(event):
    if event.fwd_from:
        return
    gbun = await edit_or_reply(event, "`Processing Gbanning...`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, gbun)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await gbun.edit("**Terjadi Kesalahan, Harap Balas Kepesanan Untuk melakukan Gbanning**")
        return
    if user.id in DEVS:
        await gbun.edit("**Gagal Melakukan Global Banning Karna Dia Adalah Pembuat Saya**")
        return
    if gban_sql.is_gbanned(user.id):
        await gbun.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Sudah Berada Di Daftar Gban List**"
        )
    else:
        gban_sql.freakgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await gbun.edit("**maaf Anda Tidak Mempunyai Hak Admin Di Group Ini**")
        return
    await gbun.edit(
        f"**initiating gban of the** [{user.first_name}](tg://user?id={user.id}) **in** `{len(san)}` **groups**"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda tidak memiliki izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await gbun.edit(
            f"**GBanned** [{user.first_name}](tg://user?id={user.id}) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Reason :** `{reason}`"
        )
    else:
        await gbun.edit(
            f"**GBanned** [{user.first_name}](tg://user?id={user.id}) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Added to gbanlist.**"
        )


@geez_cmd(pattern="ungban(?: |$)(.*)")
@register(pattern=r"^\.cungban(?: |$)(.*)", sudo=True)
async def ungban(event):
    if event.fwd_from:
        return
    ungbun = await edit_or_reply(event, "`UnGbanning...`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, ungbun)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.freakungban(user.id)
    else:
        await ungbun.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Tidak Berada Di Daftar GBan List!!!**"
        )
        return
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await ungbun.edit("**Terjadi Kesalahan Karna Anda Bukan lah admin.**")
        return
    await ungbun.edit(
        f"**initiating ungban of the** [{user.first_name}](tg://user?id={user.id}) **in** `{len(san)}` **groups**"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda tidak memiliki izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await ungbun.edit(
            f"**UngBanned** [{user.first_name}](tg://user?id={user.id}) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Reason :** `{reason}`"
        )
    else:
        await ungbun.edit(
            f"**UngBanned** [{user.first_name}](tg://user?id={user.id}) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Removed from gbanlist**"
        )


@geez_cmd(pattern="listgban$")
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "**List Global Banned Anda Saat Ini**\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) **Reason** `{a_user.reason}`\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) `No Reason`\n"
                )
    if len(gbanned_users) >= 4096:
        with BytesIO(str.encode(GBANNED_LIST)) as fileuser:
            fileuser.name = "list-gban.txt"
            await event.client.send_file(
                event.chat_id,
                fileuser,
                force_document=True,
                thumb="geezproject/resources/logo.jpg",
                caption="**List Global Banned**",
                allow_cache=False,
            )
    else:
        GBANNED_LIST = "Belum ada Pengguna yang Di-Gban"
    await edit_or_reply(event, GBANNED_LIST)


@bot.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        if gban_sql.is_gbanned(user.id) and chat.admin_rights:
            try:
                await event.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                await event.reply(
                    f"**#GBanned_User** Joined.\n\n** • First Name:** [{user.first_name}](tg://user?id={user.id})\n • **Action:** `Banned`"
                )
            except BaseException:
                pass


CMD_HELP.update(
    {
        "gban": f"**Plugin : **`gban`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}gban` <username/id>\
        \n  ❍▸ : **Melakukan Banned Secara Global Ke Semua Grup Dimana anda Sebagai Admin.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ungban` <username/id>\
        \n  ❍▸ : **Membatalkan Global Banned\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}listgban`\
        \n  ❍▸ : **Menampilkan List Global Banned\
    "
    }
)
