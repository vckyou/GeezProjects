# Thanks Full For © TeamUltroid
# Ported By @Vckyaz < GeezProjects\ >
#
# From GeezProjects < https://github.com/vckyou/GeezProjects/ >

import io
import os
import random
from os import remove

import cv2
import requests
from userbot import LOGS
from userbot.utils.tools import create_quotly, TgConverter
from telethon.errors import YouBlockedUserError
from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeSticker
from userbot.utils import edit_or_reply, geez_cmd
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP

KANGING_STR = [
    "Prosess Mengambil Sticker Pack!",
    "Mengambil Sticker Pack Anda",
    "Proses!",
    "Ijin Colong Stickernya Yaa :D",
]

@geez_cmd(pattern="vkang(?: |$)(.*)")
async def hehe(args):
    user = await args.client.get_me()
    xx = await edit_or_reply(args, "`Sedang Memproses...`")
    username = user.username
    if not username:
        username = user.first_name
    else:
        username = "@" + username
    message = await args.get_reply_message()
    photo = None
    is_anim = False
    is_vid = False
    emoji = None
    if not message:
        return await edit_or_reply(xx, "Membalas pesan/media...")
    if message.photo:
        photo = io.BytesIO()
        photo = await args.client.download_media(message.photo, photo)
    elif message.file and "image" in message.file.mime_type.split("/"):
        photo = io.BytesIO()
        await args.client.download_file(message.media.document, photo)
        if (
            DocumentAttributeFilename(file_name="sticker.webp")
            in message.media.document.attributes
        ):
            emoji = message.media.document.attributes[1].alt

    elif message.file and "video" in message.file.mime_type.split("/"):
        xy = await message.download_media()
        if (message.file.duration or 0) <= 10:
            is_vid = True
            photo = await TgConverter.create_webm(xy)
        else:
            y = cv2.VideoCapture(xy)
            heh, lol = y.read()
            cv2.imwrite("geez.webp", lol)
            photo = "geez.webp"
    elif message.file and "tgsticker" in message.file.mime_type:
        await args.client.download_file(
            message.media.document,
            "AnimatedSticker.tgs",
        )
        attributes = message.media.document.attributes
        for attribute in attributes:
            if isinstance(attribute, DocumentAttributeSticker):
                emoji = attribute.alt
        is_anim = True
        photo = 1
    elif message.message:
        photo = await create_quotly(message)
        return await xx.edit("`Unsupported File!`")
    return await xx.edit(f"`{random.choice(KANGING_STR)}`")
    if photo:
        splat = args.text.split()
        pack = 1
        if not emoji:
            emoji = "⚡"
        if len(splat) == 3:
            pack = splat[2]
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                pack = int(splat[1])
            else:
                emoji = splat[1]

        packname = f"geez_{user.id}_{pack}"
        packnick = f"{username}'s Pack {pack}"
        cmd = "/newpack"
        file = io.BytesIO()

        if is_vid:
            packname += "_vid"
            packnick += " (Video)"
            cmd = "/newvideo"
        elif is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"
        else:
            image = con.resize_photo_sticker(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")

        response = requests.get(f"http://t.me/addstickers/{packname}")
        htmlstr = response.text.split("\n")

        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with args.client.conversation("@Stickers") as conv:
                try:
                    await conv.send_message("/addsticker")
                except YouBlockedUserError:
                    LOGS.info("Unblocking @Stickers for kang...")
                    await args.client(functions.contacts.UnblockRequest("stickers"))
                    await conv.send_message("/addsticker")
                await conv.get_response()
                await conv.send_message(packname)
                x = await conv.get_response()
                if x.text.startswith("Alright! Now send me the video sticker."):
                    await conv.send_file(photo, force_document=True)
                    x = await conv.get_response()
                t = "50" if (is_anim or is_vid) else "120"
                while t in x.message:
                    pack += 1
                    packname = f"geez_{user.id}_{pack}"
                    packnick = f"{username}'s Pack {pack}"
                    if is_anim:
                        packname += "_anim"
                        packnick += " (Animated)"
                    elif is_vid:
                        packnick += " (Video)"
                        packname += "_vid"
                    await xx.edit(f"`Beralih ke Sticker Pack {pack} karena ruang yang tidak mencukupi`")
                    await conv.send_message("/addsticker")
                    await conv.get_response()
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text.startswith("Alright! Now send me the video sticker."):
                        await conv.send_file(photo, force_document=True)
                        x = await conv.get_response()
                    if x.text in ["Invalid pack selected.", "Invalid set selected."]:
                        await conv.send_message(cmd)
                        await conv.get_response()
                        await conv.send_message(packnick)
                        await conv.get_response()
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            if is_vid:
                                file = photo
                            else:
                                file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        await conv.get_response()
                        await conv.send_message("/skip")
                        await conv.get_response()
                        await conv.send_message(packname)
                        await conv.get_response()
                        await xx.edit(
                             "** Sticker Berhasil Ditambahkan!**"
                             f"\n          ⚡ **[KLIK DISINI](t.me/addstickers/{packname})** ⚡\n**Untuk Menggunakan Stickers**",
                             parse_mode="md",
                        )
                        return
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                elif "send me an emoji" not in x.message:
                    if is_vid:
                        file = photo
                    else:
                        file.seek(0)
                    await conv.send_file(file, force_document=True)
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        await xx.edit(
                            "`Gagal menambahkan stiker, gunakan bot` @Stickers `untuk menambahkan stiker secara manual.`",
                        )
                        return
                await conv.send_message(emoji)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)
        else:
            await xx.edit("`Brewing a new Pack...`")
            async with args.client.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                await conv.send_message(packnick)
                await conv.get_response()
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    if is_vid:
                        file = photo
                    else:
                        file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await xx.edit(
                        "`Gagal menambahkan stiker, gunakan bot` @Stickers `untuk menambahkan stiker secara manual.`",
                    )
                    return
                await conv.send_message(emoji)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")

                await conv.get_response()
                await conv.send_message("/skip")
                await conv.get_response()
                await conv.send_message(packname)
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)
        await xx.edit(
            f"**Kanged!**\n**Emoji :** {emoji}\n**Sticker Pack** [Lihat Disini](t.me/addstickers/{packname})",
            parse_mode="md",
        )
        try:
            os.remove(photo)
        except BaseException:
            pass


CMD_HELP.update(
    {
        "stickers_video": f"**Plugin : **`stickers_vidoe`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}vkang` [emoji]\
        \n  ↳ : **Balas .vkang Ke Sticker Atau Gambar Untuk Menambahkan Ke Sticker Pack Mu\
    "
    }
)
