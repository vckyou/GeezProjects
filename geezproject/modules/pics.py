# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Ported by @mrismanaziz
# Recode by @vckyaz
# FROM GeezProjects <https://github.com/vckyou/GeezProjects>
# Support @GeezSupport & @GeezProjects

from asyncio import sleep
from io import BytesIO

from telethon import types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import SendMediaRequest

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, bot
from geezproject.events import geez_cmd


@bot.on(geez_cmd(outgoing=True, pattern=r"pic(?: |$)(.*)"))
async def on_file_to_photo(pics):
    await pics.edit("`Processing...`")
    await sleep(1.5)
    await pics.delete()
    target = await pics.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith("image/"):
        return
    if image.mime_type == "image/webp":
        return
    if image.size > 10 * 2560 * 1440:
        return

    file = await pics.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await pics.client.upload_file(file)
    img.name = "image.png"

    try:
        await pics.client(
            SendMediaRequest(
                peer=await pics.get_input_chat(),
                media=types.InputMediaUploadedPhoto(img),
                message=target.message,
                entities=target.entities,
                reply_to_msg_id=target.id,
            )
        )
    except PhotoInvalidDimensionsError:
        return


CMD_HELP.update(
    {
        "pic": f"**Plugin : **`pic`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}pic` <reply ke file document foto>\
        \n  •  **Function : **Untuk Mengubah Gambar Dokumen apa pun menjadi Gambar Ukuran Penuh.\
    "
    }
)
