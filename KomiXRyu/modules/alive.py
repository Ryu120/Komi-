from KomiXRyu import dispatcher
from telegram import Update, ParseMode

from telegram.ext import (
    CallbackContext,
    CommandHandler,
)

PHOTO = "https://telegra.ph/file/cb3adab8257b4b2096df5.jpg"

def alive(update: Update, context: CallbackContext):
    TEXT = f"I Am 𝑺𝒉𝒐𝒖𝒌𝒐 𝑲𝒐𝒎𝒊!\n\n◈ I will love to be in your group chat ◈"
    

    update.effective_message.reply_photo(
        PHOTO, caption= TEXT,
        parse_mode=ParseMode.MARKDOWN)

ALIVE_HANDLER = CommandHandler("alive", alive, run_async = True)
dispatcher.add_handler(ALIVE_HANDLER)


__help__ = """ 
❂ /alive: To check if bot is alive or not."""
   
__mod_name__ = "Alive"
