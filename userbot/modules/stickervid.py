import io
import random
import urllib.request
from os import remove

from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    MessageMediaPhoto,
)

from userbot import CMD_HELP, bot
from userbot.utils import edit_or_reply, geez_cmd
from userbot.utils.tools import geez_webm
from userbot import CMD_HANDLER as cmd

@geez_cmd(pattern="(?:vkang|vtikel)\s?(.)?")
async def kang(args):
    """For .kang command, kangs stickers or creates new ones."""
    user = await bot.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    is_video = False
    emoji = None

    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            xx = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await bot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            xx = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await bot.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                if emoji != "":
                    emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            xx = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            await bot.download_file(message.media.document, "AnimatedSticker.tgs")

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojibypass = True
            is_anim = True
            photo = 1
        elif "video" in message.media.document.mime_type:
            await xx.edit("`Converting...`")
            vid_sticker = await geez_webm(message)
            xx = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")

            is_video = True
            photo = 1
        else:
            return await xx.edit("`Unsupported File!`")
    else:
        return await xx.edit("`I can't kang that...`")

    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "🤔"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]  # User sent both
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                # User wants to push into different pack, but is okay with
                # thonk as emote.
                pack = int(splat[1])
            else:
                # User sent just custom emote, wants to push to default
                # pack
                emoji = splat[1]

        packname = f"a{user.id}_by_{user.username}_{pack}"
        packnick = f"@{user.username}'s kang pack Vol.{pack}"
        cmd = "/newpack"
        file = io.BytesIO()

        if is_video:
            packname += "_vid"
            packnick += " (Video)"
            cmd = "/newvideo"
        elif is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"
        else:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")

        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")

        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with bot.conversation("Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packname = f"a{user.id}_by_{user.username}_{pack}"
                    packnick = f"@{user.username}'s kang pack Vol.{pack}"
                    await xx.edit(
                        "`Switching to Pack "
                        + str(pack)
                        + " due to insufficient space`"
                    )
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        elif is_video:
                            await conv.send_file(vid_input)
                            remove(vid_input)
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        return await xx.edit(
                            "`Sticker added in a Different Pack !"
                            "\nThis Pack is Newly created!"
                            f"\nYour pack can be found [here](t.me/addstickers/{packname})",
                            parse_mode="md",
                        )
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                elif is_video:
                    await conv.send_file(vid_sticker)
                    remove(vid_sticker)
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    return await xx.edit(
                        "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`"
                    )
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await args.edit("`Brewing a new Pack...`")
            async with bot.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                elif is_video:
                    await conv.send_file(vid_sticker)
                    remove(vid_sticker)
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    return await xx.edit(
                        "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`"
                    )
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)

        await xx.edit(
            "Curry Success!" f"\n[Klik Disini](t.me/addstickers/{packname})",
            parse_mode="md",
        )


CMD_HELP.update(
    {
        "stickervid": f"**Plugin : **`stickervid`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}vkang` <sambil reply ke media>\
        \n  ↳ : **Untuk Mengubah Sticker Menjadi Kecil.\
    "
    }
)