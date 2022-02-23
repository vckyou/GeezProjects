# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import GROUP
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, ICON_HELP, bot
from userbot.utils import edit_delete, edit_or_reply, geez_cmd

modules = CMD_HELP


@geez_cmd(pattern="help(?: |$)(.*)")
async def help(event):
    """For help command"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await edit_or_reply(event, str(CMD_HELP[args]))
        else:
            await edit_delete(event, f"`Maaf Module` {args}` `Tidak Dapat Ditemukan!`")
    else:
        user = await bot.get_me()
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += f"`\t\t\t{ICON_HELP}\t\t\t"
        await edit_or_reply(
            event,
            f"{ICON_HELP}   {string}"
            f"\n\nSupport @{GROUP}\n"
        )
        await event.reply(
            f"╭┄──────┈┄┈──────┄\n"
            f"│ ▸ **Daftar Perintah GeezProjects :**\n"
            f"│ ▸ **Jumlah** `{len(modules)}` **Modules**\n"
            f"│ ▸ **Owner:** [{user.first_name}](tg://user?id={user.id})\n"
            f"├┄─────┈┄┈─────┄\n"
            f"│ **Contoh Ketik** `{cmd}help ping`\n"
            f"│ **Untuk Melihat Informasi Module**\n"
            f"╰┄──────┈┈──────┄"
        )
