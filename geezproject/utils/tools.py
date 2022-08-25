# Copyright (C) 2020 Adek Maulana
#
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# recode by @vckyaz
# GeezProjects 
# <https://github.com/vckyou/GeezProjects>
#


import base64
import asyncio
import hashlib
import os
import json
import aiohttp
import os.path
import re
import shlex
import time

from os.path import basename
from typing import Optional, Union, Tuple
from io import BytesIO
from json.decoder import JSONDecodeError
from aiohttp import ContentTypeError
from emoji import get_emoji_regexp
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from html_telegraph_poster import TelegraphPoster
from PIL import Image

from telethon.utils import get_display_name, get_peer_id
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    DocumentAttributeFilename,
)
from telethon.tl import types
from yt_dlp import YoutubeDL

from geezproject import DEVS, LOGS, SUDO_USERS, TEMP_DOWNLOAD_DIRECTORY, bot
from geezproject.utils.format import md_to_text, paste_message


def deEmojify(inputString):
    return get_emoji_regexp().sub("", inputString)


async def md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def media_type(message):
    if message and message.photo:
        return "Photo"
    if message and message.audio:
        return "Audio"
    if message and message.voice:
        return "Voice"
    if message and message.video_note:
        return "Round Video"
    if message and message.gif:
        return "Gif"
    if message and message.sticker:
        return "Sticker"
    if message and message.video:
        return "Video"
    if message and message.document:
        return "Document"
    return None


def humanbytes(size: Union[int, float]) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " hari, ") if days else "")
        + ((str(hours) + " jam, ") if hours else "")
        + ((str(minutes) + " menit, ") if minutes else "")
        + ((str(seconds) + " detik, ") if seconds else "")
    )
    return tmp[:-2]


async def extract_time(geez, time_val):
    if any(time_val.endswith(unit) for unit in ("s", "m", "h", "d", "w")):
        unit = time_val[-1]
        time_num = time_val[:-1]
        if not time_num.isdigit():
            await geez.edit("Jumlah waktu yang ditentukan tidak valid.")
            return None
        if unit == "s":
            bantime = int(time.time() + int(time_num) * 1)
        elif unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        elif unit == "w":
            bantime = int(time.time() + int(time_num) * 7 * 24 * 60 * 60)
        else:
            await geez.edit(
                f"**Jenis waktu yang dimasukan tidak valid. Harap masukan** s, m , h , d atau w tapi punya: `{time_val[-1]}`"
            )
            return None
        return bantime
    await geez.edit(
        f"**Jenis waktu yang dimasukan tidak valid. Harap Masukan** s, m , h , d atau w tapi punya: `{time_val[-1]}`"
    )
    return None


def human_to_bytes(size: str) -> int:
    units = {
        "M": 2 ** 20,
        "MB": 2 ** 20,
        "G": 2 ** 30,
        "GB": 2 ** 30,
        "T": 2 ** 40,
        "TB": 2 ** 40,
    }

    size = size.upper()
    if not re.match(r" ", size):
        size = re.sub(r"([KMGT])", r" \1", size)
    number, unit = [string.strip() for string in size.split()]
    return int(float(number) * units[unit])


async def is_admin(chat_id, user_id):
    req_jo = await bot(GetParticipantRequest(channel=chat_id, user_id=user_id))
    chat_participant = req_jo.participant
    return isinstance(
        chat_participant, (ChannelParticipantCreator, ChannelParticipantAdmin)
    )


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """take a screenshot"""
    LOGS.info(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    ttl = duration // 2
    thumb_image_path = path or os.path.join("./temp/", f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


async def edit_or_reply(
    event,
    text,
    parse_mode=None,
    link_preview=None,
    file_name=None,
    aslink=False,
    deflink=False,
    noformat=False,
    linktext=None,
    caption=None,
):
    link_preview = link_preview or False
    reply_to = await event.get_reply_message()
    if len(text) < 4096 and not deflink:
        parse_mode = parse_mode or "md"
        if not event.out and event.sender_id in SUDO_USERS:
            if reply_to:
                return await reply_to.reply(
                    text, parse_mode=parse_mode, link_preview=link_preview
                )
            return await event.reply(
                text, parse_mode=parse_mode, link_preview=link_preview
            )
        await event.edit(text, parse_mode=parse_mode, link_preview=link_preview)
        return event
    if not noformat:
        text = md_to_text(text)
    if aslink or deflink:
        linktext = linktext or "**Pesan Terlalu Panjang**"
        response = await paste_message(text, pastetype="s")
        text = linktext + f" [Lihat Disini]({response})"
        if not event.out and event.sender_id in SUDO_USERS:
            if reply_to:
                return await reply_to.reply(text, link_preview=link_preview)
            return await event.reply(text, link_preview=link_preview)
        await event.edit(text, link_preview=link_preview)
        return event
    file_name = file_name or "output.txt"
    caption = caption or None
    with open(file_name, "w+") as output:
        output.write(text)
    if reply_to:
        await reply_to.reply(caption, file=file_name)
        await event.delete()
        return os.remove(file_name)
    if not event.out and event.sender_id in SUDO_USERS:
        await event.reply(caption, file=file_name)
        await event.delete()
        return os.remove(file_name)
    await event.client.send_file(event.chat_id, file_name, caption=caption)
    await event.delete()
    os.remove(file_name)


eor = edit_or_reply


async def check_media(reply_message):
    if not reply_message or not reply_message.media:
        return False

    if reply_message.photo:
        data = reply_message.photo
    elif reply_message.document:
        if (
            DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
            in reply_message.media.document.attributes
        ):
            return False
        if (
            reply_message.gif
            or reply_message.video
            or reply_message.audio
            or reply_message.voice
        ):
            return False
        data = reply_message.media.document
    else:
        return False
    if not data or data is None:
        return False
    return data


async def run_cmd(cmd: list) -> Tuple[bytes, bytes]:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await process.communicate()
    t_resp = out.strip()
    e_resp = err.strip()
    return t_resp, e_resp


# https://github.com/TeamUltroid/pyUltroid/blob/31c271cf4d35ab700e5880e952e54c82046812c2/pyUltroid/functions/helper.py#L154


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


def post_to_telegraph(title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "GeezProjects"
    auth_url = "https://github.com/vckyou/GeezProjects"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=title,
        author=auth_name,
        author_url=auth_url,
        text=html_format_content,
    )
    return post_page["url"]


def _unquote_text(text):
    return text.replace("'", "'").replace('"', '"')

def json_parser(data, indent=None):
    parsed = {}
    try:
        if isinstance(data, str):
            parsed = json.loads(str(data))
            if indent:
                parsed = json.dumps(json.loads(str(data)), indent=indent)
        elif isinstance(data, dict):
            parsed = data
            if indent:
                parsed = json.dumps(data, indent=indent)
    except JSONDecodeError:
        parsed = eval(data)
    return parsed


async def edit_delete(event, text, time=None, parse_mode=None, link_preview=None):
    parse_mode = parse_mode or "md"
    link_preview = link_preview or False
    time = time or 15
    if not event.out and event.sender_id in SUDO_USERS:
        reply_to = await event.get_reply_message()
        newevent = (
            await reply_to.reply(text, link_preview=link_preview, parse_mode=parse_mode)
            if reply_to
            else await event.reply(
                text, link_preview=link_preview, parse_mode=parse_mode
            )
        )
    else:
        newevent = await event.edit(
            text, link_preview=link_preview, parse_mode=parse_mode
        )
    await asyncio.sleep(time)
    return await newevent.delete()


eod = edit_delete


async def media_to_pic(event, reply):
    mediatype = media_type(reply)
    if mediatype not in ["Photo", "Round Video", "Gif", "Sticker", "Video"]:
        await edit_delete(
            event,
            "**Saya tidak dapat mengekstrak gambar untuk memproses lebih lanjut ke media yang tepat**",
        )
        return None
    media = await reply.download_media(file="./temp")
    event = await edit_or_reply(event, "`Transfiguration Time! Converting....`")
    file = os.path.join("./temp/", "meme.png")
    if mediatype == "Sticker":
        if media.endswith(".tgs"):
            await runcmd(
                f"lottie_convert.py --frame 0 -if lottie -of png '{media}' '{file}'"
            )
        elif media.endswith(".webp"):
            im = Image.open(media)
            im.save(file)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        extractMetadata(createParser(media))
        await runcmd(f"rm -rf '{file}'")
        await take_screen_shot(media, 0, file)
        if not os.path.exists(file):
            await edit_delete(
                event,
                f"**Maaf. Saya tidak dapat mengekstrak gambar dari ini {mediatype}**",
            )
            return None
    else:
        im = Image.open(media)
        im.save(file)
    await runcmd(f"rm -rf '{media}'")
    return [event, file, mediatype]


ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "noprogress": True,
    "user-agent": "Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "extractor-args": "youtube:player_client=all",
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download_lagu(url: str) -> str:
    info = ydl.extract_info(url, download=False)
    ydl.download([url])
    return os.path.join("downloads", f"{info['id']}.{info['ext']}")


# quotly
async def async_searcher(
    url: str,
    post: bool = None,
    headers: dict = None,
    params: dict = None,
    json: dict = None,
    data: dict = None,
    ssl=None,
    re_json: bool = False,
    re_content: bool = False,
    real: bool = False,
):
    async with aiohttp.ClientSession(headers=headers) as client:
        if post:
            data = await client.post(url, json=json, data=data, ssl=ssl)
        else:
            data = await client.get(url, params=params, ssl=ssl)
        if re_json:
            return await data.json()
        if re_content:
            return await data.read()
        if real:
            return data
        return await data.text()


_entities = {
    types.MessageEntityPhone: "phone_number",
    types.MessageEntityMention: "mention",
    types.MessageEntityBold: "bold",
    types.MessageEntityCashtag: "cashtag",
    types.MessageEntityStrike: "strikethrough",
    types.MessageEntityHashtag: "hashtag",
    types.MessageEntityEmail: "email",
    types.MessageEntityMentionName: "text_mention",
    types.MessageEntityUnderline: "underline",
    types.MessageEntityUrl: "url",
    types.MessageEntityTextUrl: "text_link",
    types.MessageEntityBotCommand: "bot_command",
    types.MessageEntityCode: "code",
    types.MessageEntityPre: "pre",
}


async def _format_quote(event, reply=None, sender=None, type_="private"):
    async def telegraph(file_):
        file = f"{file_}.png"
        Image.open(file_).save(file, "PNG")
        files = {"file": open(file, "rb").read()}
        uri = (
            "https://telegra.ph"
            + (
                await async_searcher(
                    "https://telegra.ph/upload", post=True, data=files, re_json=True
                )
            )[0]["src"]
        )
        os.remove(file)
        os.remove(file_)
        return uri

    if reply:
        reply = {
            "name": get_display_name(reply.sender) or "Deleted Account",
            "text": reply.raw_text,
            "chatId": reply.chat_id,
        }
    else:
        reply = {}
    is_fwd = event.fwd_from
    name = None
    last_name = None
    if sender and sender.id not in DEVS:
        id_ = get_peer_id(sender)
        name = get_display_name(sender)
    elif not is_fwd:
        id_ = event.sender_id
        sender = await event.get_sender()
        name = get_display_name(sender)
    else:
        id_, sender = None, None
        name = is_fwd.from_name
        if is_fwd.from_id:
            id_ = get_peer_id(is_fwd.from_id)
            try:
                sender = await event.client.get_entity(id_)
                name = get_display_name(sender)
            except ValueError:
                pass
    if sender and hasattr(sender, "last_name"):
        last_name = sender.last_name
    entities = []
    if event.entities:
        for entity in event.entities:
            if type(entity) in _entities:
                enti_ = entity.to_dict()
                del enti_["_"]
                enti_["type"] = _entities[type(entity)]
                entities.append(enti_)
    message = {
        "entities": entities,
        "chatId": id_,
        "avatar": True,
        "from": {
            "id": id_,
            "first_name": (name or (sender.first_name if sender else None))
            or "Deleted Account",
            "last_name": last_name,
            "username": sender.username if sender else None,
            "language_code": "en",
            "title": name,
            "name": name or "Unknown",
            "type": type_,
        },
        "text": event.raw_text,
        "replyMessage": reply,
    }
    if event.document and event.document.thumbs:
        file_ = await event.download_media(thumb=-1)
        uri = await telegraph(file_)
        message["media"] = {"url": uri}

    return message


O_API = "https://bot.lyo.su/quote/generate"


async def create_quotly(
    event,
    url="https://qoute-api-akashpattnaik.koyeb.app/generate",
    reply={},
    bg=None,
    sender=None,
    file_name="quote.webp",
):
    if not isinstance(event, list):
        event = [event]
        url = O_API
    if not bg:
        bg = "#1b1429"
    content = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": bg,
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": [
            await _format_quote(message, reply=reply, sender=sender)
            for message in event
        ],
    }
    try:
        request = await async_searcher(url, post=True, json=content, re_json=True)
    except ContentTypeError as er:
        if url != O_API:
            return await create_quotly(O_API, post=True, json=content, re_json=True)
        raise er
    if request.get("ok"):
        with open(file_name, "wb") as file:
            image = base64.decodebytes(request["result"]["image"].encode("utf-8"))
            file.write(image)
        return file_name
    raise Exception(str(request))


async def Carbon(
    code,
    base_url="https://carbonara-42.herokuapp.com/api/cook",
    file_name="GeezProjects",
    **kwargs,
):
    kwargs["code"] = code
    con = await async_searcher(base_url, post=True, json=kwargs, re_content=True)
    file = BytesIO(con)
    file.name = f"{file_name}.jpg"
    return file


async def animator(media, mainevent, textevent):
    # //Hope u dunt kang :/ @Jisan7509
    h = media.file.height
    w = media.file.width
    w, h = (-1, 512) if h > w else (512, -1)
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    geez = await mainevent.client.download_media(media, TEMP_DOWNLOAD_DIRECTORY)
    await textevent.edit("__🎞 Converting...__")
    await runcmd(
        f"ffmpeg -ss 00:00:00 -to 00:00:02.900 -i {geez} -vf scale={w}:{h} -c:v libvpx-vp9 -crf 30 -b:v 560k -maxrate 560k -bufsize 256k -an Video.webm"
    )  # pain
    os.remove(geez)
    vid = "Video.webm"
    return vid
