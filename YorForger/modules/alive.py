import re
import os

from telethn import events, Button
from pyrogram import __version__ as pyrover
from YorForger.events import register as MEMEK
from YorForger import telethn as tbot

PHOTO = "https://telegra.ph/file/355e0913c12a233afbe9b.jpg"

@MEMEK(pattern=("/alive"))
async def awake(event):
  tai = event.sender.first_name
  YorForger = "**Hello, I'm Yor Forger!** \n\n"
  YorForger += "×**I'm Working Properly** \n\n"
  YorForger += "×**My Darling : [AUGSTUN🝪ZECROX](https://t.me/Aug0felix)** \n\n"
  YorForger += "**My Manager : [Sneha](https://t.me/Sneha_UwU_OwO)** \n\n"
  YorForger += f"×**Telethon Version : {tlhver}** \n\n"
  YorForger += f"×**Pyrogram Version : {pyrover}** \n\n"
  YorForger += "**Thanks For Adding Me Here ❤️**"
  BUTTON = [[Button.url("ʜᴇʟᴘ", "http://t.me/Yor_forger_spyxfamily_bot?start=help"), Button.url("sᴜᴘᴘᴏʀᴛ", "https://t.me/yorforgersupportgrp")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=YorForger,  buttons=BUTTON)

@MEMEK(pattern=("/reload"))
async def reload(event):
  tai = event.sender.first_name
  YorForger = "✅ **bot restarted successfully**\n\n• Admin list has been **updated**"
  BUTTON = [[Button.url("📡 ᴜᴘᴅᴀᴛᴇs", "https://t.me/yorforgerbotupdates")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=YorForger,  buttons=BUTTON)




__mod_name__ = "Alive"
__help__ = """
*ALIVE*
 ❍ `/alive` :Check BOT status
"""
