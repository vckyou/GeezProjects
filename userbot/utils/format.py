import math
import os
import datetime

from bs4 import BeautifulSoup
from markdown import markdown
from telethon.tl.tlobject import TLObject
from telethon.tl.types import MessageEntityPre
from telethon.utils import add_surrogate

from .paste import pastetext
from .tools import bash


async def paste_message(text, pastetype="p", extension=None, markdown=True):
    if markdown:
        text = md_to_text(text)
    response = await pastetext(text, pastetype, extension)
    if "url" in response:
        return response["url"]
    return "Error while pasting text to site"


def md_to_text(md):
    html = markdown(md)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()


def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"


def htmlmentionuser(name, userid):
    return f"<a href='tg://user?id={userid}'>{name}</a>"


def reformattext(text):
    return text.replace("~", "").replace("_", "").replace("*", "").replace("`", "")


# kanged from uniborg @spechide
# https://github.com/SpEcHiDe/UniBorg/blob/d8b852ee9c29315a53fb27055e54df90d0197f0b/uniborg/utils.py#L250


def reformattext(text):
    return text.replace("~", "").replace("_", "").replace("*", "").replace("`", "")


def replacetext(text):
    return (
        text.replace(
            '"',
            "",
        )
        .replace(
            "\\r",
            "",
        )
        .replace(
            "\\n",
            "",
        )
        .replace(
            "\\",
            "",
        )
    )


def parse_pre(text):
    text = text.strip()
    return (
        text,
        [MessageEntityPre(offset=0, length=len(add_surrogate(text)), language="")],
    )


def yaml_format(obj, indent=0, max_str_len=256, max_byte_len=64):
    # sourcery no-metrics
    """
    Pretty formats the given object as a YAML string which is returned.
    (based on TLObject.pretty_format)
    """
    result = []
    if isinstance(obj, TLObject):
        obj = obj.to_dict()

    if isinstance(obj, dict):
        if not obj:
            return "dict:"
        items = obj.items()
        has_items = len(items) > 1
        has_multiple_items = len(items) > 2
        result.append(obj.get("_", "dict") + (":" if has_items else ""))
        if has_multiple_items:
            result.append("\n")
            indent += 2
        for k, v in items:
            if k == "_" or v is None:
                continue
            formatted = yaml_format(v, indent)
            if not formatted.strip():
                continue
            result.append(" " * (indent if has_multiple_items else 1))
            result.append(f"{k}:")
            if not formatted[0].isspace():
                result.append(" ")
            result.append(f"{formatted}")
            result.append("\n")
        if has_items:
            result.pop()
        if has_multiple_items:
            indent -= 2
    elif isinstance(obj, str):
        # truncate long strings and display elipsis
        result = repr(obj[:max_str_len])
        if len(obj) > max_str_len:
            result += "…"
        return result
    elif isinstance(obj, bytes):
        # repr() bytes if it's printable, hex like "FF EE BB" otherwise
        if all(0x20 <= c < 0x7F for c in obj):
            return repr(obj)
        return "<…>" if len(obj) > max_byte_len else " ".join(f"{b:02X}" for b in obj)
    elif isinstance(obj, datetime.datetime):
        # ISO-8601 without timezone offset (telethon dates are always UTC)
        return utc_to_local(obj).strftime("%Y-%m-%d %H:%M:%S")
    elif hasattr(obj, "__iter__"):
        # display iterables one after another at the base indentation level
        result.append("\n")
        indent += 2
        for x in obj:
            result.append(f"{' ' * indent}- {yaml_format(x, indent + 2)}")
            result.append("\n")
        result.pop()
        indent -= 2
    else:
        return repr(obj)

    return "".join(result)


# ------------------------#


class LottieException(Exception):
    ...


class TgConverter:
    """Convert files related to Telegram"""

    @staticmethod
    async def animated_sticker(file, out_path="sticker.tgs", throw=False, remove=False):
        """Convert to/from animated sticker."""
        if out_path.endswith("webp"):
            er, out = await bash(
                f"lottie_convert.py --webp-quality 100 --webp-skip-frames 100 '{file}' '{out_path}'"
            )
        else:
            er, out = await bash(f"lottie_convert.py '{file}' '{out_path}'")
        if er and throw:
            raise LottieException(er)
        if remove:
            os.remove(file)
        if os.path.exists(out_path):
            return out_path

    @staticmethod
    async def animated_to_gif(file, out_path="gif.gif"):
        """Convert animated sticker to gif."""
        await bash(
            f"lottie_convert.py '{_unquote_text(file)}' '{_unquote_text(out_path)}'"
        )
        return out_path

    @staticmethod
    def resize_photo_sticker(photo):
        """Resize the given photo to 512x512 (for creating telegram sticker)."""
        image = Image.open(photo)
        if (image.width and image.height) < 512:
            size1 = image.width
            size2 = image.height
            if image.width > image.height:
                scale = 512 / size1
                size1new = 512
                size2new = size2 * scale
            else:
                scale = 512 / size2
                size1new = size1 * scale
                size2new = 512
            size1new = math.floor(size1new)
            size2new = math.floor(size2new)
            sizenew = (size1new, size2new)
            image = image.resize(sizenew)
        else:
            maxsize = (512, 512)
            image.thumbnail(maxsize)
        return image

    @staticmethod
    async def ffmpeg_convert(input_, output, remove=False):
        if output.endswith(".webm"):
            return await TgConverter.create_webm(
                input_, name=output[:-5], remove=remove
            )
        await bash(f"ffmpeg -i '{input_}' '{output}' -y")
        if remove:
            os.remove(input_)
        if os.path.exists(output):
            return output

    @staticmethod
    async def create_webm(file, name="video", remove=False):
        _ = await metadata(file)
        name += ".webm"
        h, w = _["height"], _["width"]
        if h == w and h != 512:
            h, w = 512, 512
        if h != 512 or w != 512:
            if h > w:
                h, w = 512, -1
            if w > h:
                h, w = -1, 512
        await bash(
            f'ffmpeg -i "{file}" -preset fast -an -to 00:00:02.95 -crf 30 -bufsize 256k -b:v {_["bitrate"]} -vf scale={w}:{h} -c:v libvpx-vp9 "{name}" -y'
        )
        if remove:
            os.remove(file)
        return name

    @staticmethod
    def to_image(input_, name, remove=False):
        img = cv2.VideoCapture(input_)
        ult, roid = img.read()
        cv2.imwrite(name, roid)
        if remove:
            os.remove(input_)
        return name

    @staticmethod
    async def convert(
        input_file,
        outname="converted",
        convert_to=None,
        allowed_formats=[],
        remove_old=True,
    ):
        if "." in input_file:
            ext = input_file.split(".")[-1].lower()
        else:
            return input_file

        if (
            ext in allowed_formats
            or ext == convert_to
            or not (convert_to or allowed_formats)
        ):
            return input_file

        def recycle_type(exte):
            return convert_to == exte or exte in allowed_formats

        # Sticker to Something
        if ext == "tgs":
            for extn in ["webp", "json", "png", "mp4", "gif"]:
                if recycle_type(extn):
                    name = outname + "." + extn
                    return await TgConverter.animated_sticker(
                        input_file, name, remove=remove_old
                    )
            if recycle_type("webm"):
                input_file = await TgConverter.convert(
                    input_file, convert_to="gif", remove_old=remove_old
                )
                return await TgConverter.create_webm(input_file, outname, remove=True)
        # Json -> Tgs
        elif ext == "json":
            if recycle_type("tgs"):
                name = outname + ".tgs"
                return await TgConverter.animated_sticker(
                    input_file, name, remove=remove_old
                )
        # Video to Something
        elif ext in ["webm", "mp4", "gif"]:
            for exte in ["webm", "mp4", "gif"]:
                if recycle_type(exte):
                    name = outname + "." + exte
                    return await TgConverter.ffmpeg_convert(
                        input_file, name, remove=remove_old
                    )
            for exte in ["png", "jpg", "jpeg", "webp"]:
                if recycle_type(exte):
                    name = outname + "." + exte
                    return TgConverter.to_image(input_file, name, remove=remove_old)
        # Image to Something
        elif ext in ["jpg", "jpeg", "png", "webp"]:
            for extn in ["png", "webp", "ico"]:
                if recycle_type(extn):
                    img = Image.open(input_file)
                    name = outname + "." + extn
                    img.save(name, extn.upper())
                    if remove_old:
                        os.remove(input_file)
                    return name
            for extn in ["webm", "gif", "mp4"]:
                if recycle_type(extn):
                    name = outname + "." + extn
                    if extn == "webm":
                        input_file = await TgConverter.convert(
                            input_file,
                            convert_to="png",
                            remove_old=remove_old,
                        )
                    return await TgConverter.ffmpeg_convert(
                        input_file, name, remove=True if extn == "webm" else remove_old
                    )


# --------- END --------- #
