# Copyright (C) 2020  @deleteduser420 <https://github.com/code-rgb>
# ported by @mrismanaziz
# recode by @vckyaz
# FROM GeezProjects <https://github.com/vckyou/GeezProjects>
# Support @GeezSupport & @GeezProjects
import os

import requests

from geezproject import CMD_HELP, DEEP_AI, bot
from geezproject.events import geez_cmd
from geezproject.utils import edit_delete, edit_or_reply


@bot.on(geez_cmd(outgoing=True, pattern=r"detect$"))
async def detect(event):
    if DEEP_AI is None:
        return await edit_delete(
            event,
            "**Tambahkan VAR** `DEEP_AI` **dan ambil Api Key di web https://deepai.org/**",
            120,
        )
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "**Mohon Reply ke gambar atau stiker!**", 90)
    coy = await edit_or_reply(event, "**MenDownload file untuk diperiksa...**")
    media = await event.client.download_media(reply)
    if not media.endswith(("png", "jpg", "webp")):
        return await edit_delete(event, "**Mohon Reply ke gambar atau stiker!**", 90)
    coy = await edit_or_reply(event, "**Detecting NSFW limit...**")
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            "image": open(media, "rb"),
        },
        headers={"api-key": DEEP_AI},
    )
    os.remove(media)
    if "status" in r.json():
        return await edit_delete(coy, r.json()["status"])
    r_json = r.json()["output"]
    pic_id = r.json()["id"]
    percentage = r_json["nsfw_score"] * 100
    detections = r_json["detections"]
    link = f"https://api.deepai.org/job-view-file/{pic_id}/inputs/image.jpg"
    result = f"<b>Detected Nudity :</b>\n<a href='{link}'>>>></a> <code>{percentage:.3f}%</code>\n\n"
    if detections:
        for parts in detections:
            name = parts["name"]
            confidence = int(float(parts["confidence"]) * 100)
            result += f"<b>• {name}:</b>\n   <code>{confidence} %</code>\n"
    await edit_or_reply(
        coy,
        result,
        link_preview=False,
        parse_mode="HTML",
    )


CMD_HELP.update(
    {
        "nsfw": "**Plugin : **`nsfw`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.detect` <reply media>\
        \n  ❍▸ : **Untuk mendeteksi konten 18+ dengan gambar balasan.\
    "
    }
)
