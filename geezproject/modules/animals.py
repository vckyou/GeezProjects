# Taken from
# https://github.com/AvinashReddy3108/PaperplaneRemix/blob/master/geezproject/plugins/memes.py

# TG-geezproject - A modular Telegram geezproject script for Python.
# Copyright (C) 2019 Kandarp <https://github.com/kandnub>
#
# TG-geezproject is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TG-geezproject is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TG-geezproject.  If not, see <https://www.gnu.org/licenses/>.

import requests

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP
from geezproject.utils import edit_or_reply, geez_cmd


@geez_cmd(pattern="shibe$")
async def shibe(event):
    xx = await edit_or_reply(event, "`Processing...`")
    response = requests.get("https://shibe.online/api/shibes").json()
    if not response:
        await event.edit("**Tidak bisa menemukan Anjing.**")
        return
    await event.client.send_message(entity=event.chat_id, file=response[0])
    await xx.delete()


@geez_cmd(pattern="cat$")
async def cats(event):
    xx = await edit_or_reply(event, "`Processing...`")
    response = requests.get("https://shibe.online/api/cats").json()
    if not response:
        await event.edit("**Tidak bisa menemukan kucing.**")
        return
    await event.client.send_message(entity=event.chat_id, file=response[0])
    await xx.delete()

CMD_HELP.update(
    {
        "animals": f"**Plugin : **`animals`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}cat`\
        \n  ↳ : **Untuk Mengirim gambar kucing secara random.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}shibe`\
        \n  ↳ : **Untuk Mengirim gambar random dari anjing jenis Shiba.\
    "
    }
)
