import asyncio

from telethon.tl.functions.channels import EditAdminRequest, InviteToChannelRequest
from telethon.tl.types import ChatAdminRights

from geezproject import BOT_VER as version
from geezproject import BOTLOG_CHATID
from geezproject import CMD_HANDLER as cmd
from geezproject import GEEZ2, GEEZ3, GEEZ4, GEEZ5, bot, branch

MSG_ON = """
     __⚡ Congratulations ⚡__
__GeezProhects Has Been Deployed__
─┄───┅───┄─
▸ **geezproject Version -** `{}@{}`
▸ **Ketik** `{}ping` **untuk Mengecheck Bot**
─┄───┅───┄─
"""


async def geez_userbot_on():
    new_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    try:
        if bot and tgbot:
            GEEZAV = await tgbot.get_me()
            BOT_USERNAME = GEEZAV.username
            await bot(InviteToChannelRequest(int(BOTLOG_CHATID), [BOT_USERNAME]))
            await asyncio.sleep(3)
    except BaseException:
        pass
    try:
        if bot and tgbot:
            GEEZAV = await tgbot.get_me()
            BOT_USERNAME = GEEZAV.username
            await bot(EditAdminRequest(BOTLOG_CHATID, BOT_USERNAME, new_rights, "BOT"))
            await asyncio.sleep(3)
    except BaseException:
        pass
    try:
        if bot:
            if BOTLOG_CHATID != 0:
                await bot.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        if GEEZ2:
            if BOTLOG_CHATID != 0:
                await GEEZ2.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        if GEEZ3:
            if BOTLOG_CHATID != 0:
                await GEEZ3.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        if GEEZ4:
            if BOTLOG_CHATID != 0:
                await GEEZ4.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        if GEEZ5:
            if BOTLOG_CHATID != 0:
                await GEEZ5.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        await bot(InviteToChannelRequest(int(BOTLOG_CHATID), [BOT_USERNAME]))
    except BaseException:
        pass
