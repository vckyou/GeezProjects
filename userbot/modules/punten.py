from time import sleep

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.events import geez_cmd


@geez_cmd(geez_cmd(outgoing=True, pattern=r"sadboy(?: |$)(.*)"))
async def _(event):
    await edit_or_reply("`Pertama-tama kamu cantik`")
    sleep(2)
    await edit_or_reply("`Kedua kamu manis`")
    sleep(1)
    await edit_or_reply("`Dan yang terakhir adalah kamu bukan jodohku`")


# Create by myself @localheart


@geez_cmd(geez_cmd(outgoing=True, pattern=r"punten(?: |$)(.*)"))
async def _(event):
    await edit_or_reply(
        "`\n┻┳|―-∩`"
        "`\n┳┻|     ヽ`"
        "`\n┻┳|    ● |`"
        "`\n┳┻|▼) _ノ`"
        "`\n┻┳|￣  )`"
        "`\n┳ﾐ(￣ ／`"
        "`\n┻┳T￣|`"
        "\n**Punten**"
    )


@geez_cmd(geez_cmd(outgoing=True, pattern=r"pantau(?: |$)(.*)"))
async def _(event):
    await edit_or_reply(
        "`\n┻┳|―-∩`"
        "`\n┳┻|     ヽ`"
        "`\n┻┳|    ● |`"
        "`\n┳┻|▼) _ノ`"
        "`\n┻┳|￣  )`"
        "`\n┳ﾐ(￣ ／`"
        "`\n┻┳T￣|`"
        "\n**Masih Gua Pantau**"
    )


# Create by myself @localheart


CMD_HELP.update(
    {
        "punten": f"**Plugin : **`Animasi Punten`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}punten` ; `{cmd}pantau`\
        \n  ❍▸ : **Arts Beruang kek lagi mantau.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}sadboy`\
        \n  ❍▸ : **ya sadboy coba aja.\
    "
    }
)
