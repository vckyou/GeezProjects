# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
#
# Recode by @VckyouuBitch
# From Geez - Projects <https://github.com/vckyou/Geez-geezproject>
# 
#


import io
import os
import re
import sys
import urllib
from os import environ, execle
from time import sleep

import requests
from bs4 import BeautifulSoup
from heroku3 import from_key
from PIL import Image

from geezproject import BOT_VER, BOTLOG_CHATID
from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME, SUDO_USERS, branch
from geezproject.utils import edit_or_reply, geez_cmd, time_formatter

# ================= CONSTANT =================
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    HEROKU_APP = from_key(HEROKU_API_KEY).apps()[HEROKU_APP_NAME]
else:
    HEROKU_APP = None
# ============================================

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.70 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@geez_cmd(pattern="sleep ([0-9]+)$")
async def sleepybot(time):
    if time.sender_id in SUDO_USERS:
        return
    counter = int(time.pattern_match.group(1))
    xx = await edit_or_reply(time, "`Saya mengantuk dan tertidur...`")
    if BOTLOG_CHATID:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"**Anda menyuruh bot untuk tidur selama** {str_counter}.",
        )
    sleep(counter)
    await xx.edit("**Oke, saya sudah bangun sekarang.**")


@geez_cmd(pattern="shutdown$")
async def shutdown_bot(event):
    if event.fwd_from:
        return
    if event.sender_id in SUDO_USERS:
        return
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            "**#SHUTDOWN** \n"
            "**GeezProjects** telah di matikan!\nJika ingin menghidupkan kembali silahkan buka heroku",
        )
    await edit_or_reply(event, "**GeezProjects Berhasil di matikan!**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@geez_cmd(pattern="restart$")
async def restart_bot(event):
    if event.sender_id in SUDO_USERS:
        return
    await edit_or_reply(event, "**GeezProjects Berhasil di Restart**")
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID, "#RESTART \n" "**GeezProjects Berhasil Di Restart**"
        )
    args = [sys.executable, "-m", "geezproject"]
    execle(sys.executable, *args, environ)


@geez_cmd(pattern="readme$")
async def reedme(event):
    await edit_or_reply(
        event,
        "**Berikut sesuatu untuk kamu baca:**\n"
        "\n🔸 [geezproject Repo](https://github.com/vckyou/GeezProjects/blob/master/README.md)"
        "\n🔸 [List Variabel Heroku untuk Geez-geezproject](https://telegra.ph/List-Variable-Heroku-Untuk-GeezProjects-01-31)"
        "\n🔸 [Setup Guide - LastFM Module](https://telegra.ph/How-to-set-up-LastFM-module-for-Paperplane-geezproject-11-02)",
    )


@geez_cmd(pattern="repeat (.*)")
async def repeat(event):
    cnt, txt = event.pattern_match.group(1).split(" ", 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for _ in range(replyCount - 1):
        replyText += toBeRepeated + "\n"

    await edit_or_reply(event, replyText)


@geez_cmd(pattern="repo$")
async def repo_is_here(event):
    xx = await edit_or_reply(event, "`Processing...`")
    await xx.edit(
        f"╭‒─‒──────────────\n"
        f"│    __Thanks For Using Me__\n"
        f"├‒─‒─────────────\n"
        f"│`Bot Ver    :` `{BOT_VER}@{branch}`\n"
        f"│`Support    :` [Geez Support](t.me/GeezSupport)\n"
        f"│`Channel    :` [Channel Support](t.me/GeezProject)\n"
        f"│`Owner Repo :` [vickyaz](t.me/vckyaz)\n"
        f"├‒─‒──────────────\n"
        f"│`Repository :` [𝙂𝙚𝙚𝙯 𝙋𝙧𝙤𝙟𝙚𝙘𝙩𝙨](https://github.com/Vckyou/GeezProjects)\n"
        f"╰‒─‒─────────────\n"
        f"  𝗟𝗶𝗰𝗲𝗻𝘀𝗲 : [GPL-3.0 License](https://github.com/Vckyou/GeezProjects/blob/master/LICENSE)"
    )


@geez_cmd(pattern="string$")
async def string_is_here(event):
    await edit_or_reply(
        event,
        "**GET STRING SESSION TELEGRAM :** [KLIK DISINI](https://repl.it/@vckyou/String?lite=1&outputonly=1)\n",
    )


@geez_cmd(pattern="raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await edit_or_reply(
            event, "`Check the geezproject log for the decoded message data !!`"
        )
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="**Inilah data pesan yang didecodekan !!**",
        )


@geez_cmd(pattern="reverse(?: |$)(\d*)")
async def okgoogle(img):
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")
    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await img.client.download_media(message, photo)
    else:
        return await edit_or_reply(img, "**Harap Balas ke Gambar**")
    if photo:
        xx = await edit_or_reply(img, "`Processing...`")
        try:
            image = Image.open(photo)
        except OSError:
            await xx.edit("**Gambar tidak di dukung**")
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers["Location"]
        if response != 400:
            await xx.edit(
                "`Image successfully uploaded to Google. Maybe.`"
                "\n`Parsing source now. Maybe.`"
            )
        else:
            return await xx.edit("**Google told me to fuck off.**")
        os.remove(name)
        match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
        guess = match["best_guess"]
        imgspage = match["similar_images"]
        if guess and imgspage:
            await xx.edit(f"[{guess}]({fetchUrl})\n\n`Looking for images...`")
        else:
            await xx.edit("**Tidak dapat menemukan apa pun.**")
            return
        lim = img.pattern_match.group(1) or 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await img.client.send_file(
                entity=await img.client.get_input_entity(img.chat_id),
                file=yeet,
                reply_to=img,
            )
        except TypeError:
            pass
        await xx.edit(
            f"[{guess}]({fetchUrl})\n\n[Gambar yang mirip secara visual]({imgspage})"
        )


async def ParseSauce(googleurl):
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}
    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass
    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()
    return results


async def scam(results, lim):
    single = opener.open(results["similar_images"]).read()
    decoded = single.decode("utf-8")
    imglinks = []
    counter = 0
    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)
    for imglink in oboi:
        counter += 1
        if counter < int(lim):
            imglinks.append(imglink)
        else:
            break
    return imglinks


@geez_cmd(pattern="send (.*)")
async def send(event):
    if not event.is_reply:
        return await edit_or_reply(
            event, "**Mohon Balas ke pesan yang ingin dikirim!**"
        )
    chat = event.pattern_match.group(1)
    xx = await edit_or_reply(event, "**Berhasil Mengirim pesan ini**")
    try:
        chat = int(chat)
    except ValueError:
        pass
    try:
        chat = await event.client.get_entity(chat)
    except (TypeError, ValueError):
        return await xx.edit("**Link yang diberikan tidak valid!**")
    message = await event.get_reply_message()
    await event.client.send_message(entity=chat, message=message)
    await xx.edit(f"**Berhasil Mengirim pesan ini ke** `{chat.title}`")


CMD_HELP.update(
    {
        "send": f"**Plugin : **`send`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}send` <username/id>\
        \n  ❍▸ : **Meneruskan pesan balasan ke obrolan tertentu tanpa tag Forwarded from. Bisa mengirim ke Group Chat atau ke Personal Message\
    "
    }
)

CMD_HELP.update(
    {
        "random": f"**Plugin : **`random`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}random`\
        \n  ❍▸ : **Dapatkan item acak dari daftar item. \
    "
    }
)

CMD_HELP.update(
    {
        "sleep": f"**Plugin : **`sleep`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}sleep`\
        \n  ❍▸ : **Biarkan GeezProjects tidur selama beberapa detik \
    "
    }
)


CMD_HELP.update(
    {
        "repo": f"**Plugin : **`Repository GeezProjects`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}repo`\
        \n  ❍▸ : **Menampilan link Repository GeezProjects\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}string`\
        \n  ❍▸ : **Menampilan link String GeezProjects\
    "
    }
)


CMD_HELP.update(
    {
        "readme": f"**Plugin : **`Panduan Menggunakan geezproject`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}readme`\
        \n  ❍▸ : **Menyediakan tautan untuk mengatur geezproject dan modulnya\
    "
    }
)


CMD_HELP.update(
    {
        "restart": f"**Plugin : **`Restart GeezProjects`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}restart`\
        \n  ❍▸ : **Untuk Merestart geezproject.\
    "
    }
)


CMD_HELP.update(
    {
        "shutdown": f"**Plugin : **`shutdown`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}shutdown`\
        \n  ❍▸ : **Mematikan geezproject.\
    "
    }
)


CMD_HELP.update(
    {
        "raw": f"**Plugin : **`raw`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}raw`\
        \n  ❍▸ : **Dapatkan data berformat seperti JSON terperinci tentang pesan yang dibalas.\
    "
    }
)


CMD_HELP.update(
    {
        "repeat": f"**Plugin : **`repeat`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}repeat`\
        \n  ❍▸ : **Mengulangi teks untuk beberapa kali. Jangan bingung ini dengan spam tho.\
    "
    }
)
