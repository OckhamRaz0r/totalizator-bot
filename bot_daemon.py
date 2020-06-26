#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import \
    ReplyKeyboardRemove,\
    Update

from telegram.ext import \
    Updater,\
    CommandHandler,\
    MessageHandler,\
    Filters,\
    ConversationHandler,\
    CallbackContext

from modules import \
    LogHandler,\
    handle_errors,\
    AdminConversationHandler,\
    UserConversationHandler

import time
import json
import os

# ENVIRONMENTS
AUTH = json.load(open('./auth.json', 'r'))
TOKEN = AUTH.get('TOKEN', '')
ROOT = int(AUTH.get('ROOT', 0))
ADMINS = list(int(_) for _ in AUTH.get('ADMINS', []))

DB_HOST = os.environ.get('DB_HOST', "127.0.0.1")
DB_PORT = int(os.environ.get('DB_PORT', 27017))
AUTH_DB_NAME = os.environ.get('AUTH_DB_NAME', "")
DATA_DB_NAME = os.environ.get('AUTH_DB_NAME', "")

# FILTERS
RootFilter = Filters.user(ROOT)

# GLOBAL VARS
SHUTDOWN = False

# LOGGING
logger = LogHandler()


def error(update: Update, context: CallbackContext):
    logger.error(context.error)


@handle_errors
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Ola! Everything seems to be ok.. yee, i know, it looks strange",
        reply_markup=ReplyKeyboardRemove())


@handle_errors
def reboot(update: Update, context: CallbackContext):
    global SHUTDOWN
    update.message.reply_text(f"Rebooting..",
                              reply_markup=ReplyKeyboardRemove())
    SHUTDOWN = True


@handle_errors
def stats(update: Update, context: CallbackContext):
    update.message.reply_text(f"admins: {len(ADMINS)}\n",
                              reply_markup=ReplyKeyboardRemove())


RootConversationHandler = ConversationHandler(
    entry_points=[
        CommandHandler('start', echo, filters=RootFilter),
        CommandHandler('reboot', reboot, filters=RootFilter),
        CommandHandler('stats', stats, filters=RootFilter),
    ],
    states={},
    fallbacks=[],
    per_chat=True,
)


if __name__ == '__main__':
    """Start the bot"""
    # create the EventHandler and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # get the dispatcher to register handlers
    dp = updater.dispatcher

    # conversation handlers
    dp.add_handler(RootConversationHandler)
    dp.add_handler(AdminConversationHandler)
    # dp.add_handler(UserConversationHandler)

    # log all errors
    dp.add_error_handler(error)

    # start the Bot
    updater.start_polling()

    # notification of successfully start
    updater.bot.send_message(
        chat_id=ROOT,
        text=f'Ready!\nConnected to DBs:\n'
             f'{DB_HOST}:{DB_PORT}[{AUTH_DB_NAME}]\n'
             f'{DB_HOST}:{DB_PORT}[{DATA_DB_NAME}]\n'
    )

    while not SHUTDOWN:
        time.sleep(0.5)

    updater.stop()
