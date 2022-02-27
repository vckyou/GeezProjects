# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Copyright (C) 2021 TeamUltroid for autobot
""" Userbot start point """

import sys
from importlib import import_module

import requests
from pytgcalls import idle
from telethon.tl.functions.channels import InviteToChannelRequest

from userbot import BOT_TOKEN, BOT_USERNAME, BOT_VER, BOTLOG_CHATID
from userbot import DEVS, LOGS, bot, branch, call_py
from userbot.modules import ALL_MODULES
from userbot.utils import autobot, checking

try:
    bot.start()
    call_py.start()
    user = bot.get_me()
    blacklistgeez = requests.get(
        "https://raw.githubusercontent.com/vckyou/Reforestation/master/blacklistgeez.json"
    ).json()
    if user.id in blacklistgeez:
        LOGS.warning(
            "NAMPAKNYA USERBOT TIDAK DAPAT BEKERJA, MUNGKIN ANDA TELAH DI BLACKLIST OLEH PEMILIK USERBOT.\nCredits: @VckyouuBitch"        )
        sys.exit(1)
    if 5155140917 not in DEVS:
        LOGS.warning(
            f"EOL\nGeezProjects v{BOT_VER}, Copyright © 2021-2022 VICKY <https://github.com/vckyou>"
        )
        sys.exit(1)
except Exception as e:
    LOGS.info(str(e), exc_info=True)
    sys.exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(
    f"Jika {user.first_name} Membutuhkan Bantuan, Silahkan Tanyakan di Grup https://t.me/GeezSupport"
)

LOGS.info(f"💢 Geez - Projects Berhasil Diaktfikan 💢",
            )

async def geez_userbot_on():
    try:
        if BOTLOG_CHATID != 0:
            await bot.send_message(
                BOTLOG_CHATID,
                f"💢 Geez - Projects Berhasil Diaktfikan 💢\n╼┅━━━━━╍━━━━━┅╾\n❍▹ Bot Of : {user.first_name}\n❍▹ BotVer : {BOT_VER}@{branch}\n╼┅━━━━━╍━━━━━┅╾",
            )
    except Exception as e:
        LOGS.info(str(e))
    try:
        await bot(InviteToChannelRequest(int(BOTLOG_CHATID), [BOT_USERNAME]))
    except BaseException:
        pass


bot.loop.run_until_complete(checking())
bot.loop.run_until_complete(geez_userbot_on())
if not BOT_TOKEN:
    bot.loop.run_until_complete(autobot())
idle()
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
