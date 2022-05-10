import html

import json
import os
from typing import Optional

from YorForger import (DEV_USERS, OWNER_ID, SUPPORT_USERS, WHITELIST_USERS, dispatcher)
from YorForger.modules.helper_funcs.chat_status import (dev_plus, sudo_plus,
                                                           ass_plus)
from YorForger.modules.helper_funcs.extraction import extract_user
from YorForger.modules.log_channel import loggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(),
                                   'YorForger/elevated_users.json')


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka baka!"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
#disasters =
# """ Text here """

# do not async, not a handler
#def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends

#FtSasaki adding add to pro developer cmd :D

@run_async
@dev_plus
@loggable
def addpiro(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)
        
    if int(user_id) in DEV_USERS:
      message.reply_text("This member is already my Spy")
        
    if user_id in SUPPORT_USERS:
        rt += "Requested to Darling to promote a Family Member to Spy."
        data['sudos'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        rt += "Requested to Darling to promote my Target to Spy."
        data['whitelist'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    data['devs'].append(user_id)
    DEV_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfull {} He is my Spy!".format(
            user_member.first_name))

    log_message = (
        f"#ProDeveloper\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_plus
@loggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUPPORT_USERS:
        message.reply_text("This member is already my Family Member")
        return ""

    if user_id in WHITELIST_USERS:
        rt += "Requested to Darling to promote my Target to Family Member."
        data['whitelist'].remove(user_id)
        WHITELIST_USERS.remove(user_id)


    data['sudos'].append(user_id)
    SUPPORT_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfull {} is my Family Member!".format(
            user_member.first_name))

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@loggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUPPORT_USERS:
        rt += "Requested Darling to demote him to Family Member to Target"
        data['sudos'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        message.reply_text("This user is already a Target.")
        return ""


    data['whitelist'].append(user_id)
    WHITELIST_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as my Target!")

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



#FtSasaki adding rmpiro to remove user from {devs}
@run_async
@dev_plus
@loggable
def rmpiro(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DEV_USERS:
        message.reply_text("Requested Darling to demote this user to Normal User")
        DEV_USERS.remove(user_id)
        data['devs'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNDEV\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not my Target!")
        return ""
      
      
@run_async
@dev_plus
@loggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUPPORT_USERS:
        message.reply_text("Requested Darling to demote this user to Normal User")
        SUPPORT_USERS.remove(user_id)
        data['sudos'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not my Family Member!")
        return ""


@run_async
@sudo_plus
@loggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WHITELIST_USERS:
        message.reply_text("Requested Darling to demote this user to Normal user")
        WHITELIST_USERS.remove(user_id)
        data['whitelist'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not my Target!")
        return ""




DEV_HANDLER = CommandHandler(("addspy", "adddev"), addpiro)
SUDO_HANDLER = CommandHandler(("addagent", "adddrag"), addsudo)
SUPPORT_HANDLER = CommandHandler(("addfamilymember", "addsupport"), addsupport)

RMPIRO_HANDLER = CommandHandler(("rmspy", "rmdev"), rmpiro)
UNSUDO_HANDLER = CommandHandler(("rmagent", "rmsudo"), removesudo)
UNSUPPORT_HANDLER = CommandHandler(("rmfamilymember", "removesupp"),
                                   removesupport)

dispatcher.add_handler(DEV_HANDLER)
dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(RMPIRO_HANDLER)

__mod_name__ = "Disasters"
__handlers__ = [
    DEV_HANDLER, SUDO_HANDLER, SUPPORT_HANDLER, UNSUDO_HANDLER, UNSUPPORT_HANDLER, RMPIRO_HANDLER]
