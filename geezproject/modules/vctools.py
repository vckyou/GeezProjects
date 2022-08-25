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
# Support @GeezSupport & @GeezProject
# 

from pytgcalls import StreamType
from pytgcalls.exceptions import AlreadyJoinedError
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, owner, call_py
from geezproject.events import register
from geezproject.utils import edit_delete, edit_or_reply, geez_cmd


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


@geez_cmd(pattern="vcinvite")
async def _(c):
    xxnx = await edit_or_reply(c, "`Inviting Members to Voice Chat...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    geez = list(user_list(users, 6))
    for p in geez:
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

# credits by @vckyaz < vicky \>
# FROM GeezProjects < https://github.com/vckyou/GeezProjects \>
# ambil boleh apus credits jangan ya ka:)


@geez_cmd(pattern="joinvc(?: |$)(.*)")
@register(pattern=r"^\.joinvcs(?: |$)(.*)", sudo=True)
async def joinvc(event):
    geez = await edit_or_reply(event, "`Processing...`")
    if len(event.text.split()) > 1:
        chat_id = event.text.split()[1]
        try:
            chat_id = await event.client.get_peer_id(int(chat_id))
        except Exception as e:
            return await geez.edit(f"**ERROR:** `{e}`")
    else:
        chat_id = event.chat_id
    if chat_id:
        file = "./geezproject/resources/geezmusic.mp3"
        try:
            await call_py.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
            await geez.edit(
                f"• `Berhasil Naik Ke Voice Chat Group!`"
            )
        except AlreadyJoinedError:
            return await edit_delete(
                geez, f"**INFO:** `Akun Anda Sudah Berada Di VC Group!`\n\n**Noted :** __Silahkan Ketik__ `{cmd}joinvc` __untuk menggunakan command kembali.`", 30
            )
        except Exception as e:
            return await geez.edit(f"**INFO:** `{e}`")

@geez_cmd(pattern="leavevc(?: |$)(.*)")
@register(pattern=r"^\.leavevcs(?: |$)(.*)", sudo=True)
async def leavevc(event):
    geezav = await edit_or_reply(event, "`Processing...`")
    if len(event.text.split()) > 1:
        chat_id = event.text.split()[1]
        try:
            chat_id = await event.client.get_peer_id(int(chat_id))
        except Exception as e:
            return await geez.edit(f"**ERROR:** `{e}`")
    else:
        chat_id = event.chat_id
    if chat_id:
        try:
            await call_py.leave_group_call(chat_id)
            await edit_delete(
                geezav,
                f"• Anda Berhasil Turun Dari VC Group!",
            )
        except Exception as e:
            await geezav.edit(f"**INFO:** `{e}`")


CMD_HELP.update(
    {
        "vcg": f"**Plugin : **`vcg`\
        \n\n  Command :** `{cmd}startvc`\
        \n  • : **Untuk Memulai voice chat group\
        \n\n  Command :** `{cmd}stopvc`\
        \n  • : **Untuk Memberhentikan voice chat group\
        \n\n  Command :** `{cmd}vctitle` <title vcg>\
        \n  • : **Untuk Mengubah title/judul voice chat group\
        \n\n  Command :** `{cmd}vcinvite`\
        \n  • : **Mengundang Member group ke voice chat group\
        \n\n  Command :** `{cmd}joinvc`\
        \n  • : Untuk Join VC Group\
        \n\n  Command :** `{cmd}leavevc`\
        \n  • : Untuk Turun Dari VC Group\
    "
    }
)
