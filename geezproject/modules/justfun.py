# Based Plugins
# Ported For Lord-geezproject By liualvinas/Alvin
# If You Kang It Don't Delete / Warning!! Jangan Hapus Ini!!!
from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, bot
from geezproject.events import geez_cmd


@bot.on(geez_cmd(outgoing=True, pattern=r"xogame(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    botusername = "@xobot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


# Alvin Gans


@bot.on(geez_cmd(outgoing=True, pattern=r"wp(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    wwwspr = event.pattern_match.group(1)
    botusername = "@whisperBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, wwwspr)
    await tap[0].click(event.chat_id)
    await event.delete()


# Alvin Gans


@bot.on(geez_cmd(outgoing=True, pattern=r"mod(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    modr = event.pattern_match.group(1)
    botusername = "@PremiumAppBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, modr)
    await tap[0].click(event.chat_id)
    await event.delete()


# Ported For Lord-geezproject By liualvinas/Alvin


CMD_HELP.update(
    {
        "justfun": f"**Plugin : **`justfun`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}xogame`\
        \n  ❍▸ : **Game xogame bot\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}mod <nama app>`\
        \n  ❍▸ : **Dapatkan applikasi mod\
    "
    }
)


CMD_HELP.update(
    {
        "secretchat": f"**Plugin : **`secretchat`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}wp <teks> <username/ID>`\
        \n  ❍▸ : **Memberikan pesan rahasia haya orang yang di tag yang bisa melihat\
    "
    }
)
