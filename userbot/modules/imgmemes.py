"""  Some Modules Imported by @Nitesh_231 :) & Again @heyworld roks *_* """
import asyncio
import os
import re

import requests
from html_telegraph_poster.upload_images import upload_image
from PIL import Image, ImageDraw, ImageFont
from telegraph import exceptions, upload_file
from validators.url import url
from wget import download

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.utils import edit_delete, edit_or_reply, geez_cmd
from userbot.utils import bash, deEmojify


def convert_toimage(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    os.remove(image)
    return "temp.jpg"


async def threats(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trash(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trap(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def phss(uplded, input, name):
    web = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={uplded}&text={input}&username={name}"
    ).json()
    alf = web.get("message")
    uri = url(alf)
    if not uri:
        return "check syntax once more"
    with open("alf.png", "wb") as f:
        f.write(requests.get(alf).content)
    img = Image.open("alf.png").convert("RGB")
    img.save("alf.jpg", "jpeg")
    return "alf.jpg"


async def trumptweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.jpg", "jpeg")
    return "gpx.jpg"


async def changemymind(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.jpg", "jpeg")
    return "gpx.jpg"


async def kannagen(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.webp", "webp")
    return "gpx.webp"


async def moditweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=narendramodi"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def tweets(text1, text2):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.jpg", "jpeg")
    return "gpx.jpg"


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    return user_obj


async def purge():
    try:
        await bash("rm -rf *.png *.webp")
    except OSError:
        pass


@geez_cmd(pattern="trump$")
async def trump(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_or_reply("`Send you text to trump so he can tweet.`")
            return
    await edit_or_reply("`Requesting trump to tweet...`")
    text = deEmojify(text)
    img = await trumptweet(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@geez_cmd(pattern="modi$")
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_or_reply("Send you text to modi so he can tweet.")
            return
    await edit_or_reply("Requesting modi to tweet...")
    text = deEmojify(text)
    file = await moditweet(text)
    await event.client.send_file(event.chat_id, file, reply_to=reply_to_id)
    await event.delete()
    await purge()


@geez_cmd(pattern="cmm$")
async def cmm(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_or_reply("`Give text for to write on banner!`")
            return
    await edit_or_reply("`Your banner is under creation wait a sec...`")
    text = deEmojify(text)
    img = await changemymind(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@geez_cmd(pattern="kanna$")
async def kanna(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_or_reply("`What should kanna write give text!`")
            return
    await edit_or_reply("`Kanna is writing your text...`")
    text = deEmojify(text)
    img = await kannagen(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@geez_cmd(pattern="tweet$")
async def tweet(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await edit_or_reply("`What should i tweet? Give your username and tweet!`")
                return
        else:
            await edit_or_reply("What should i tweet? Give your username and tweet!`")
            return
    if "." in text:
        username, text = text.split(".", 1)
    else:
        await edit_or_reply("`What should i tweet? Give your username and tweet!`")
    await edit_or_reply(f"`Requesting {username} to tweet...`")
    text = deEmojify(text)
    img = await tweets(text, username)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@geez_cmd(pattern="threat$")
async def nekobot(event):
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await edit_or_reply("reply to a supported media file")
        return
    if replied.media:
        await edit_or_reply("passing to telegraph...")
    else:
        await edit_or_reply("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await edit_or_reply(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await edit_or_reply("generating image..")
    else:
        await edit_or_reply("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await edit_or_reply("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await threats(file)
    await event.delete()
    await bot.send_file(event.chat_id, file, reply_to=replied)


@geez_cmd(pattern="trash$")
async def nekobot(event):
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await edit_or_reply("reply to a supported media file")
        return
    if replied.media:
        await edit_or_reply("passing to telegraph...")
    else:
        await edit_or_reply("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await edit_or_reply(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await edit_or_reply("generating image..")
    else:
        await edit_or_reply("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await edit_or_reply("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await trash(file)
    await event.delete()
    await bot.send_file(event.chat_id, file, reply_to=replied)


@geez_cmd(pattern="trap$")
async def nekobot(e):
    input_str = e.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "|" in input_str:
        text1, text2 = input_str.split("|")
    else:
        await e.edit(
            "Balas Ke Gambar Atau Sticker Lalu Ketik `.trap (Nama Orang Yang Di Trap)|(Nama Trap)`"
        )
        return
    replied = await e.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await e.edit("reply to a supported media file")
        return
    if replied.media:
        await e.edit("passing to telegraph...")
    else:
        await e.edit("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await e.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await e.edit("generating image..")
    else:
        await e.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await e.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await trap(text1, text2, file)
    await e.delete()
    await bot.send_file(e.chat_id, file, reply_to=replied)


# Ported by @AshSTR


@geez_cmd(pattern="fgs$")
async def FakeGoogleSearch(event):
    """Get a user-customised google search meme!"""
    input_str = event.pattern_match.group(1)
    if input_str is None:
        await edit_or_reply("No input found!", del_in=5)
        return
    if ";" in input_str:
        search, result = input_str.split(";", 1)
    else:
        await edit_or_reply("Invalid Input! Check help for more info!", del_in=5)
        return

    await edit_or_reply("Connecting to `https://www.google.com/` ...")
    await asyncio.sleep(2)
    img = "https://i.imgur.com/wNFr5X2.jpg"
    r = download(img)
    photo = Image.open(r)
    drawing = ImageDraw.Draw(photo)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    font1 = ImageFont.truetype("userbot/utils/styles/ProductSans-BoldItalic.ttf", 20)
    font2 = ImageFont.truetype("userbot/utils/styles/ProductSans-Light.ttf", 23)
    drawing.text((450, 258), result, fill=blue, font=font1)
    drawing.text((270, 37), search, fill=black, font=font2)
    photo.save("downloads/test.jpg")
    reply = event.pattern_match.group(2)
    await event.delete()
    reply_id = event.pattern_match.group(3) if reply else None
    await event.client.send_file(
        event.chat_id, "downloads/test.jpg", reply_to_message_id=reply_id
    )
    os.remove("downloads/test.jpg")


@geez_cmd(pattern="ph$")
async def phcomment(event):
    try:
        await edit_or_reply("`Processing..`")
        text = event.pattern_match.group(1)
        reply = await event.get_reply_message()
        if reply:
            user = await get_user_from_event(event)
            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name
            text = text or str(reply.message)
        elif text:
            user = await bot.get_me()
            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name
        else:
            return await edit_or_reply("`Give text..`")
        try:
            photo = await event.client.download_profile_photo(
                user.id,
                str(user.id) + ".png",
                download_big=False,
            )
            uplded = upload_image(photo)
        except BaseException:
            uplded = "https://telegra.ph/file/7d110cd944d54f72bcc84.jpg"
    except BaseException as e:
        await purge()
        return await edit_or_reply(f"`Error: {e}`")
    img = await phss(uplded, text, name)
    try:
        await event.client.send_file(
            event.chat_id,
            img,
            reply_to=event.reply_to_msg_id,
        )
    except BaseException:
        await purge()
        return await edit_or_reply("`Reply message has no text!`")
    await event.delete()
    await purge()


CMD_HELP.update(
    {
        "imgmeme": f"**Plugin : **`imgmeme`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fgs`\
        \n  ❍▸ : **Meme dari search google yang di bisa custom user!\
        \n  •  **Example  : **`{cmd}fgs [Teks Atas] ; [Teks Bawah]`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}trump`\
        \n  ❍▸ : **Membuat Tweet dari akun twitter Donald Trump\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}modi` <text>\
        \n  ❍▸ : **Membuat Tweet dari akun twitter @narendramodi\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}cmm` <text>\
        \n  ❍▸ : **Membuat meme change my mind\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}kanna` <text>\
        \n  ❍▸ : **Membuat meme tulisan dari nana anime bawa kertas\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ph` <text>\
        \n  ❍▸ : **Membuat Tweet dari website pornhub\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}threat` <text> (sambil reply media foto/sticker)\
        \n  ❍▸ : **Membuat meme 3 hoax terbesar\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}trash` <text> (sambil reply media foto/sticker)\
        \n  ❍▸ : **Membuat meme list sampah\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}trap` <text> (sambil reply media foto/sticker)\
        \n  ❍▸ : **Membuat meme trapcard\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}tweet`\
        \n  ❍▸ : **Membuat Tweet dari akun twitter\
        \n  •  **Example  : **{cmd}tweet @vckyaz.ganteng (harus pake . [titik])\
    "
    }
)
