from base64 import b64decode

import telethon.utils
from telethon.tl.functions.users import GetFullUserRequest


async def clients_list(SUDO_USERS, bot, GEEZ2, GEEZ3, GEEZ4, GEEZ5):
    user_ids = list(SUDO_USERS) or []
    main_id = await bot.get_me()
    user_ids.append(main_id.id)

    try:
        if GEEZ2 is not None:
            id2 = await GEEZ2.get_me()
            user_ids.append(id2.id)
    except BaseException:
        pass

    try:
        if GEEZ3 is not None:
            id3 = await GEEZ3.get_me()
            user_ids.append(id3.id)
    except BaseException:
        pass

    try:
        if GEEZ4 is not None:
            id4 = await GEEZ4.get_me()
            user_ids.append(id4.id)
    except BaseException:
        pass

    try:
        if GEEZ5 is not None:
            id5 = await GEEZ5.get_me()
            user_ids.append(id5.id)
    except BaseException:
        pass

    return user_ids


ITSME = list(map(int, b64decode("NTE1NTE0MDkxNw==").split()))


async def client_id(event, botid=None):
    if botid is not None:
        uid = await event.client(GetFullUserRequest(botid))
        OWNER_ID = uid.user.id
        GEEZ_USER = uid.user.first_name
    else:
        client = await event.client.get_me()
        uid = telethon.utils.get_peer_id(client)
        OWNER_ID = uid
        GEEZ_USER = client.first_name
    geeza_mention = f"[{GEEZ_USER}](tg://user?id={OWNER_ID})"
    return OWNER_ID, GEEZ_USER, geez_mention
