# fix by @heyworld for OUB
# bug fixed by @d3athwarrior
# recode by @vckyaz
# FROM GeezProjects <https://github.com/vckyou/GeezProjects>
#
# Support @GeezSupport & @GeezProjects

from telethon.tl.types import InputMediaDice

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, bot
from geezproject.events import geez_cmd


@bot.on(geez_cmd(outgoing=True, pattern=r"dice(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice(""))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(""))
        except BaseException:
            pass


@bot.on(geez_cmd(outgoing=True, pattern=r"dart(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎯"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎯"))
        except BaseException:
            pass


@bot.on(geez_cmd(outgoing=True, pattern=r"basket(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🏀"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🏀"))
        except BaseException:
            pass


@bot.on(geez_cmd(outgoing=True, pattern=r"bowling(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎳"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎳"))
        except BaseException:
            pass


@bot.on(geez_cmd(outgoing=True, pattern=r"ball(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("⚽"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("⚽"))
        except BaseException:
            pass


@bot.on(geez_cmd(outgoing=True, pattern=r"jackpot(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎰"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎰"))
        except BaseException:
            pass


CMD_HELP.update(
    {
        "emojigames": f"**Plugin : **`emojigames`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}dice` 1-6\
        \n  ❍▸ : **Memainkan emoji game dice dengan score yg di tentukan kita.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}dart` 1-6\
        \n  ❍▸ : **Memainkan emoji game dart dengan score yg di tentukan kita.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}basket` 1-5\
        \n  ❍▸ : **Memainkan emoji game basket dengan score yg di tentukan kita.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}bowling` 1-6\
        \n  ❍▸ : **Memainkan emoji game bowling dengan score yg di tentukan kita.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ball` 1-5\
        \n  ❍▸ : **Memainkan emoji game ball telegram score yg di tentukan kita.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}jackpot` 1\
        \n  ❍▸ : **Memainkan emoji game jackpot dengan score yg di tentukan kita.\
        \n\n  •  **NOTE: **Jangan gunakan nilai lebih atau bot akan Crash**\
    "
    }
)
