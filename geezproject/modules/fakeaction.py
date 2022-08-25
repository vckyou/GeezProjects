# Ultroid - geezproject
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# recode by @vckyaz
# FROM GeezProjects <https://github.com/vckyou/GeezProjects>
#
# Support @GeezSupport & @GeezProjects

import asyncio
import math
import time

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP
from geezproject.utils import edit_delete, extract_time, geez_cmd


@geez_cmd(
    pattern="f(typing|audio|contact|document|game|location|photo|round|sticker|video) ?(.*)"
)
async def _(e):
    act = e.pattern_match.group(1)
    t = e.pattern_match.group(2)
    if act in ["audio", "round", "video"]:
        act = "record-" + act
    if t.isdigit():
        t = int(t)
    elif t.endswith(("s", "h", "d", "m")):
        t = math.ceil((await extract_time(e, t)) - time.time())
    else:
        t = 60
    await edit_delete(e, f"**Memulai fake {act} selama** `{t}` **detik**", 3)
    async with e.client.action(e.chat_id, act):
        await asyncio.sleep(t)


CMD_HELP.update(
    {
        "fakeaction": f"**Plugin :** `fakeaction`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ftyping`  <jumlah detik>\
        \n  ❍▸ :** Menampilkan Pengetikan Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}faudio` <jumlah detik>\
        \n  ❍▸ :** Menampilkan Tindakan Merekam suara Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fvideo` <jumlah detik>\
        \n  ❍▸ :** Menampilkan Tindakan Merekam Video Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fround` <jumlah detik>\
        \n  ❍▸ :** Menampilkan Tindakan Merekam Live Video Round Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fgame` <jumlah detik>\
        \n  ❍▸ :** Menampilkan sedang bermain game Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fphoto` <jumlah detik>\
        \n  ❍▸ :** Menampilkan Tindakan Mengirim Photo Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fdocument` <jumlah detik>\
        \n  ❍▸ :** Menampilkan Tindakan Mengirim Document/File Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}flocation` <jumlah detik>\
        \n  ❍▸ :** Menampilkan Tindakan Share Lokasi Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fcontact` <jumlah detik>\
        \n  ❍▸ :** Menampilkan Tindakan Share Contact Palsu dalam obrolan\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fsticker` <jumlah detik>\
        \n  ❍▸ :** Menampilkan Tindakan Memilih Sticker Palsu dalam obrolan\
    "
    }
)
