import asyncio

import socket

from asyncio import get_running_loop

from functools import partial

from aiohttp import ClientSession

from zeldris import pbot

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram import filters

sexion = ClientSession()

def _netcat(host, port, content):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.sendall(content.encode())

    s.shutdown(socket.SHUT_WR)

    while True:

        data = s.recv(4096).decode("utf-8").strip("\n\x00")

        if not data:

            break

        return data

    s.close()

async def paste_queue(content):

    loop = get_running_loop()

    link = await loop.run_in_executor(

        None, partial(_netcat, "ezup.dev", 9999, content)

    )

    return link

async def isPreviewUp(preview: str) -> bool:

    for _ in range(7):

        try:

            async with sexion.head(preview, timeout=2) as resp:

                status, size = resp.status, resp.content_length

        except asyncio.exceptions.TimeoutError:

            return False

        if status == 404 or (status == 200 and size == 0):

            await asyncio.sleep(0.4)

        else:

            return True if status == 200 else False

    return False

@pbot.on_message(filters.command("ezup"))
async def zu(client, message):
  msg = message.reply_to_message
  limk = await paste_queue(msg)
  preview = limk + "/preview.png"
  den = limk + "/index.txt"
  buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton(text="Check It Out", url={den})]
    ])
  if await isPreviewUp(preview):

                await message.reply_photo(

                    photo=preview,

                    caption="Here it is",
                    
                    quote=False,

                    reply_markup=buttons,

                )
      
  else :
    await message.reply_text(
      text= "Here it is",
      quote=False,
      reply_markup=buttons,
      )
    



     
  
  
