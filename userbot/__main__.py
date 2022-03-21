""" Userbot start point """


import sys
from importlib import import_module
from platform import python_version

from pytgcalls import __version__ as pytgcalls
from pytgcalls import idle
from telethon import version

from userbot import BOT_TOKEN
from userbot import BOT_VER as ubotversion
from userbot import LOGS, bot
from userbot.clients import geez_userbot_on, multigeez
from userbot.modules import ALL_MODULES
from userbot.utils import autobot, checking

try:
    for module_name in ALL_MODULES:
        imported_module = import_module(f"userbot.modules.{module_name}")
    client = multigeez()
    total = 5 - client
    LOGS.info(f"Total Clients = {total} User")
    LOGS.info(f"Python Version - {python_version()}")
    LOGS.info(f"Telethon Version - {version.__version__}")
    LOGS.info(f"PyTgCalls Version - {pytgcalls.__version__}")
    LOGS.info(f"GeezProjects Version - {ubotversion} < GeezProjects Berhasil Diaktfikan \>")
except BaseException as e:
    LOGS.info(str(e), exc_info=True)
    sys.exit(1)


bot.loop.run_until_complete(checking())
bot.loop.run_until_complete(geez_userbot_on())
if not BOT_TOKEN:
    bot.loop.run_until_complete(autobot())
idle()
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
