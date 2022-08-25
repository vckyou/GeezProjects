""" geezproject module for other small commands. """
from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP
from geezproject.utils import edit_or_reply, geez_cmd


@geez_cmd(pattern="listvar$")
async def var(event):
    await edit_or_reply(
        event,
        "**Daftar Lengkap Vars Dari GeezProjects:** [KLIK DISINI](https://telegra.ph/List-Variabel-Heroku-untuk-GeezProjects-09-22)",
    )


CMD_HELP.update(
    {
        "helper": f"**Plugin : **`helper`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ihelp`\
        \n  ❍▸ : **Bantuan Untuk GeezProjects.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}listvar`\
        \n  ❍▸ : **Melihat Daftar Vars.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}repo`\
        \n  ❍▸ : **Melihat Repository GeezProjects.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}string`\
        \n  ❍▸ : **Link untuk mengambil String GeezProjects.\
    "
    }
)
