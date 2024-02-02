import os
import traceback
import datetime
from pyrogram import Client, filters, types as t
from modules.utils.misc import getFileId
from modules.utils.api import isNsfw

@Client.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=9,
)
async def NSFW(_: Client, message: t.Message):
    if not message.from_user:
        return
    fileId = getFileId(message)
    if not fileId:
        return
    file = await _.download_media(fileId)
    unsafe = await isNsfw(file)
    if unsafe is True:
        try:
            await message.delete()
        except Exception:
            traceback.print_exc()
            return
    else:
        return
