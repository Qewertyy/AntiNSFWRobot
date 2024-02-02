# Copyright 2024 Qewertyy, MIT License
from PIL import Image
import asyncio,base64,mimetypes,os,hashlib,base64
from lexica import AsyncClient
from functools import wraps
import httpx,re,traceback
from urllib.parse import urlsplit
from modules.database import isNSFW,addFileHash
from modules.utils.misc import upload

def getContentType(url):
    """Get Media Content Type"""
    try:
        client = httpx.Client()
        response = client.head(url)
        if response.status_code != 200:
            return None
        return response.headers['content-type'].split("/")[0]
    except (TimeoutError, httpx.ReadTimeout,httpx.ReadError,httpx.ConnectTimeout):
        return None


async def Check(file):
    img_url = await upload(file)
    if img_url is None:
        return
    client = AsyncClient()
    try:
        output = await client.AntiNsfw(img_url)
        await client.close()
    except (TimeoutError, httpx.ReadTimeout,httpx.ReadError,httpx.ConnectTimeout):
        return None
    except Exception as e:
        print("Failed:",e)
        return None
    return output

def convertToPNG(image):
    im = Image.open(image)
    im.save(image, "PNG")

def getFileHash(file):
    hashs = hashlib.sha256()
    with open(file,"rb") as img:
        while chunk := img.read(4096):
            hashs.update(chunk)
        img.close()
    fileHash = hashs.hexdigest()
    return fileHash

async def isNsfw(file: str):
    """
    Check if file is NSFW
    """
    fileHash = getFileHash(file)
    if isNSFW(fileHash) is True:
        os.remove(file)
        return True
    else:
        for i in ["jpg","jpeg","webp"]:
            if file.endswith(i):
                convertToPNG(file) # cause telegraph acts weird sometimes.
        result = await Check(file)
        if result is None or result['code'] != 2:
            return
        sfw = result['content']['sfw']
        if sfw == True:
            return False
        else:
            await addNsfwFile(fileHash)
            return True

async def addNsfwFile(fileHash):
    return await addFileHash(fileHash)