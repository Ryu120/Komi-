
from io import BytesIO
from time import sleep

from telegram import TelegramError
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler

import KomiXRyu.modules.sql.users_sql as sql
from KomiXRyu import dispatcher, LOGGER, DEV_USERS
from KomiXRyu.modules.helper_funcs.filters import CustomFilters

USERS_GROUP = 4
CHAT_GROUP = 10


def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith("@"):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    if len(users) == 1:
        return users[0].user_id
    for user_obj in users:
        try:
            userdat = dispatcher.bot.get_chat(user_obj.user_id)
            if userdat.username == username:
                return userdat.id

        except BadRequest as excp:
            if excp.message == "Chat not found":
                pass
            else:
                LOGGER.exception("Error extracting user ID")

    return None


def broadcast(update, context):
    if update.effective_message.reply_to_message:
      to_send=update.effective_message.reply_to_message.message_id
    if not update.effective_message.reply_to_message:
      return update.effective_message.reply_text("Reply To Some Shit To Broadcast")
    chats = sql.get_all_chats() or []
    users = sql.get_all_users() or []
    failed = 0
    for chat in chats:
      try:
        context.bot.forwardMessage(chat_id=int(chat.chat_id), from_chat_id=update.effective_chat.id, message_id=to_send)
        sleep(0.1)
      except TelegramError:
        failed += 1
        LOGGER.warning("Couldn't send broadcast to %s, group name %s", str(chat.chat_id), str(chat.chat_name),)

    failed_user = 0
    for user in users:
      try:
        context.bot.forwardMessage(chat_id=int(user.user_id), from_chat_id=update.effective_chat.id, message_id=to_send)
        sleep(0.1)
      except TelegramError:
        failed_user += 1
        LOGGER.warning("Couldn't send broadcast to %s, group name %s", str(user.user_id), str(user.username),)


    update.effective_message.reply_text("Broadcast complete. {} groups failed to receive the message, probably due to being kicked. {} users failed to receive the message, probably due to being banned.".format(failed, failed_user))


def log_user(update, _):
    chat = update.effective_chat
    msg = update.effective_message

    sql.update_user(msg.from_user.id, msg.from_user.username, chat.id, chat.title)

    if msg.reply_to_message:
        sql.update_user(
            msg.reply_to_message.from_user.id,
            msg.reply_to_message.from_user.username,
            chat.id,
            chat.title,
        )

    if msg.forward_from:
        sql.update_user(msg.forward_from.id, msg.forward_from.username)


@sudo_plus
def chats(update: Update, context: CallbackContext):
    all_chats = sql.get_all_chats() or []
    chatfile = "List of chats.\n0. Chat name | Chat ID | Members count\n"
    P = 1
    for chat in all_chats:
        try:
            curr_chat = context.bot.getChat(chat.chat_id)
            bot_member = curr_chat.get_member(context.bot.id)
            chat_members = curr_chat.get_member_count(context.bot.id)
            chatfile += "{}. {} | {} | {}\n".format(
                P,
                chat.chat_name,
                chat.chat_id,
                chat_members,
            )
            P = P + 1
        except:
            pass

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "groups_list.txt"
        update.effective_message.reply_document(
            document=output,
            filename="groups_list.txt",
            caption="Here be the list of groups in my database.",
        )


def chat_checker(update: Update, context: CallbackContext):
    bot = context.bot
    try:
        if update.effective_message.chat.get_member(bot.id).can_send_messages is False:
            bot.leaveChat(update.effective_message.chat.id)
    except Unauthorized:
        pass


def __user_info__(user_id):
    if user_id in [777000, 5327104856]:
        return """╘═━「 Groups count: <code>???</code> 」"""
    if user_id == dispatcher.bot.id:
        return """╘═━「 Groups count: <code>???</code> 」"""
    num_chats = sql.get_user_num_chats(user_id)
    return f"""╘═━「 Groups count: <code>{num_chats}</code> 」"""


def __stats__():
    return f"× {sql.num_users()} users, across {sql.num_chats()} chats"


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


__help__ = ""  # no help string

BROADCAST_HANDLER = CommandHandler(
    ["broadcastall", "broadcastusers", "broadcastgroups"],
    broadcast,
    run_async=True,
)
USER_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, log_user, run_async=True
)
CHAT_CHECKER_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, chat_checker, run_async=True
)
CHATLIST_HANDLER = CommandHandler("groups", chats, run_async=True)

dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
dispatcher.add_handler(BROADCAST_HANDLER)
dispatcher.add_handler(CHATLIST_HANDLER)
dispatcher.add_handler(CHAT_CHECKER_HANDLER, CHAT_GROUP)

__mod_name__ = "Users"
__handlers__ = [(USER_HANDLER, USERS_GROUP), BROADCAST_HANDLER, CHATLIST_HANDLER]
