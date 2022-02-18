import math
import os

from userbot.utils.tools import bash
from userbot.utils.tools import metadata
from userbot import LOGS

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image, ImageDraw, ImageFont = None, None, None
    LOGS.info("PIL not installed!")
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
