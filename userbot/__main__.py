""" Userbot start point """


import sys
from importlib import import_module

from pytgcalls import idle

from userbot import BOT_TOKEN
from userbot import DEVS, LOGS, bot
from userbot.clients import geez_userbot_on, multigeez
from userbot.modules import ALL_MODULES
from userbot.utils import autobot, checking

try:
    client = multigeez()
    total = 5 - client
    bot.start()
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

    LOGS.info(f"Total Clients = {total} User")
    LOGS.info(f"Jika {user.first_name} Membutuhkan Bantuan, Silahkan Tanyakan di Grup https://t.me/GeezSupport")
    LOGS.info(f"💢 Geez - Projects Berhasil Diaktfikan 💢")

bot.loop.run_until_complete(checking())
bot.loop.run_until_complete(geez_userbot_on())
if not BOT_TOKEN:
    bot.loop.run_until_complete(autobot())
idle()
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
