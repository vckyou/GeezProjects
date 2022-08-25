# created by @eve_enryu

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP
from geezproject.utils import edit_or_reply, geez_cmd


@geez_cmd(pattern="firmware(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    firmware = "firmware"
    chat = "@XiaomiGeeksBot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{firmware} {link}")
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/{firmware} {link}")
            response = await response
        else:
            await event.delete()
            await event.client.forward_messages(event.chat_id, response.message)


@geez_cmd(pattern="fastboot(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    fboot = "fastboot"
    chat = "@XiaomiGeeksBot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{fboot} {link}")
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/{fboot} {link}")
            response = await response
        else:
            await event.delete()
            await event.client.forward_messages(event.chat_id, response.message)


@geez_cmd(pattern="recovery(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    recovery = "recovery"
    chat = "@XiaomiGeeksBot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{recovery} {link}")
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/{recovery} {link}")
            response = await response
        else:
            await event.delete()
            await event.client.forward_messages(event.chat_id, response.message)


@geez_cmd(pattern="pb(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    pitch = "pb"
    chat = "@XiaomiGeeksBot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{pitch} {link}")
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/{pitch} {link}")
            response = await response
        else:
            await event.delete()
            await event.client.forward_messages(event.chat_id, response.message)


@geez_cmd(pattern="of(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    ofox = "of"
    chat = "@XiaomiGeeksBot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{ofox} {link}")
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/{ofox} {link}")
            response = await response
        else:
            await event.delete()
            await event.client.forward_messages(event.chat_id, response.message)


@geez_cmd(pattern="eu(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    eu = "eu"
    chat = "@XiaomiGeeksBot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{eu} {link}")
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/{eu} {link}")
            response = await response
        else:
            await event.delete()
            await event.client.forward_messages(event.chat_id, response.message)


@geez_cmd(pattern="vendor(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    vendor = "vendor"
    chat = "@XiaomiGeeksBot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{vendor} {link}")
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/{vendor} {link}")
            response = await response
        else:
            await event.delete()
            await event.client.forward_messages(event.chat_id, response.message)


@geez_cmd(pattern="specs(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    specs = "specs"
    chat = "@XiaomiGeeksBot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{specs} {link}")
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/{specs} {link}")
            response = await response
        else:
            await event.delete()
            await event.client.forward_messages(event.chat_id, response.message)


CMD_HELP.update(
    {
        "xiaomi": f"**Plugin : **`xiaomi`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}firmware` (codename)\
        \n  •  **Function : **Get lastest Firmware.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}pb` (codename)\
        \n  •  **Function : **Get latest PitchBlack Recovery.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}specs` (codename)\
        \n  •  **Function : **Get quick spec information about device.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}fastboot` (codename)\
        \n  •  **Function : **Get latest fastboot MIUI.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}recovery` (codename)\
        \n  •  **Function : **Get latest recovery MIUI.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}eu` (codename)\
        \n  •  **Function : **Get latest xiaomi.eu rom.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}vendor` (codename)\
        \n  •  **Function : **fetches latest vendor.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}of` (codename)\
        \n  •  **Function : **Get latest ORangeFox Recovery.\
    "
    }
)
