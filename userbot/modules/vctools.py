# thanks full for © TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by @vckyaz
#
# FROM GeezProjects <https://github.com/vckyou/GeezProjects>
#
# Support @GeezSupport & @GeezProjects
# 

from pytgcalls import GroupCallFactory
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, owner
from userbot.events import register
from userbot.utils import edit_delete, edit_or_reply, geez_cmd


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call, limit=1))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@geez_cmd(pattern="startvc$")
@register(pattern=r"^\.startvcs$", sudo=True)
async def start_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await edit_delete(c, f"**Maaf {owner} Bukan Admin 👮**")
        return
    try:
        await c.client(startvc(c.chat_id))
        await edit_or_reply(c, "`Voice Chat Started...`")
    except Exception as ex:
        await edit_delete(c, f"**ERROR:** `{ex}`")


@geez_cmd(pattern="stopvc$")
@register(pattern=r"^\.stopvcs$", sudo=True)
async def stop_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await edit_delete(c, f"**Maaf {owner} Bukan Admin 👮**")
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await edit_or_reply(c, "`Voice Chat Stopped...`")
    except Exception as ex:
        await edit_delete(c, f"**ERROR:** `{ex}`")


@geez_cmd(pattern="joinvc$")
@register(pattern=r"^\.joinvcs$", sudo=True)
async def joinvc(event):
    xx = await event.edit("`...`")

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        await xx.edit(f"`Tidak ada obrolan, mulai dengan {cmd}startvc`")
        await sleep(15)
        return await NotUBot.delete()

    group_call = GROUP_CALLS.get(event.chat.id)
    if group_call is None:
        group_call = GroupCallFactory(
            event.client,
            GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON,
            enable_logs_to_console=False,
            path_to_log_file=None,
        ).get_file_group_call(None)
        GROUP_CALLS[event.chat.id] = group_call

    if not (group_call and group_call.is_connected):
        await group_call.start(event.chat.id, enable_action=False)

    await xx.edit("`joined`")
    await sleep(3)
    await xx.delete()


@geez_cmd(pattern="leavevc$")
@register(pattern=r"^\.leavevcs$", sudo=True)
async def leavevc(event):
    xx = await event.edit("`...`")

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        await xx.edit(f"`Tidak ada obrolan, mulai dengan {cmd}startvc`")
        await sleep(15)
        return await xx.delete()

    group_call = GROUP_CALLS.get(event.chat.id)
    if group_call and group_call.is_connected:
        await group_call.leave_current_group_call()
        await group_call.stop()

    await xx.edit("`leaved`")
    await sleep(3)
    await xx.delete()


@geez_cmd(pattern="vcinvite")
async def _(c):
    xxnx = await edit_or_reply(c, "`Inviting Members to Voice Chat...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    botman = list(user_list(users, 6))
    for p in botman:
        try:
            await c.client(invitetovc(call=await get_call(c), users=p))
            z += 6
        except BaseException:
            pass
    await xxnx.edit(f"`{z}` **Orang Berhasil diundang ke VCG**")


@geez_cmd(pattern="vctitle(?: |$)(.*)")
@register(pattern=r"^\.cvctitle$", sudo=True)
async def change_title(e):
    title = e.pattern_match.group(1)
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await edit_delete(e, "**Silahkan Masukan Title Obrolan Suara Grup**")

    if not admin and not creator:
        await edit_delete(e, f"**Maaf {owner} Bukan Admin 👮**")
        return
    try:
        await e.client(settitle(call=await get_call(e), title=title.strip()))
        await edit_or_reply(e, f"**Berhasil Mengubah Judul VCG Menjadi** `{title}`")
    except Exception as ex:
        await edit_delete(e, f"**ERROR:** `{ex}`")


CMD_HELP.update(
    {
        "vcg": f"**Plugin : **`vcg`\
        \n\n   :** `{cmd}startvc`\
        \n   : **Untuk Memulai voice chat group\
        \n\n   :** `{cmd}stopvc`\
        \n   : **Untuk Memberhentikan voice chat group\
        \n\n   :** `{cmd}vctitle` <title vcg>\
        \n   : **Untuk Mengubah title/judul voice chat group\
        \n\n   :** `{cmd}vcinvite`\
        \n   : **Mengundang Member group ke voice chat group\
    "
    }
)
