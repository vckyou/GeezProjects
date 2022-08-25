from time import sleep

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, owner
from geezproject.utils import edit_or_reply, geez_cmd


@geez_cmd(pattern="p(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**Assalamualaikum Dulu Biar Sopan**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@geez_cmd(pattern="pe(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**Assalamualaikum Warahmatullahi Wabarakatuh**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@geez_cmd(pattern="P(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**Haii Salken Saya {owner}**")
    sleep(2)
    await xx.edit("**Assalamualaikum...**")


@geez_cmd(pattern="l(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id, "**Wa'alaikumsalam**", reply_to=event.reply_to_msg_id
    )
    await event.delete()


@geez_cmd(pattern="a(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**Haii Salken Saya {owner}**")
    sleep(2)
    await xx.edit("**Assalamualaikum**")


@geez_cmd(pattern="j(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "**JAKA SEMBUNG BAWA GOLOK**")
    sleep(3)
    await xx.edit("**NIMBRUNG GOBLOKK!!!🔥**")


@geez_cmd(pattern="k(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**Hallo KIMAAKK SAYA {owner}**")
    sleep(2)
    await xx.edit("**LU SEMUA NGENTOT 🔥**")


@geez_cmd(pattern="ass(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "**Salam Dulu Biar Sopan**")
    sleep(2)
    await xx.edit("**السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ**")


CMD_HELP.update(
    {
        "salam": f"**Plugin : **`salam`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}p`\
        \n  ❍▸ : **Assalamualaikum Dulu Biar Sopan..\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}pe`\
        \n  ❍▸ : **salam Kenal dan salam\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}l`\
        \n  ❍▸ : **Untuk Menjawab salam\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ass`\
        \n  ❍▸ : **Salam Bahas arab\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}semangat`\
        \n  ❍▸ : **Memberikan Semangat.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ywc`\
        \n  ❍▸ : **nMenampilkan Sama sama\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}sayang`\
        \n  ❍▸ : **Kata I Love You.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}k`\
        \n  ❍▸ : **LU SEMUA NGENTOT 🔥\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}j`\
        \n  ❍▸ : **NIMBRUNG GOBLOKK!!!🔥\
    "
    }
)
