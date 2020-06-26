#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import \
    ReplyKeyboardMarkup,\
    ReplyKeyboardRemove,\
    Update

from telegram.ext import \
    Updater,\
    CommandHandler,\
    MessageHandler,\
    Filters,\
    ConversationHandler,\
    CallbackContext

from .utils import \
    LogHandler,\
    handle_errors

from .models import \
    Challenge, \
    Match, \
    User, \
    Authentication

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
DATA_DB_NAME = os.environ.get('DATA_DB_NAME', "")

# MODELS
ChallengeCls = Challenge({'DB_HOST': DB_HOST, 'DB_PORT': DB_PORT, 'DB_NAME': DATA_DB_NAME})
MatchCls = Match({'DB_HOST': DB_HOST, 'DB_PORT': DB_PORT, 'DB_NAME': DATA_DB_NAME})
UserCls = User({'DB_HOST': DB_HOST, 'DB_PORT': DB_PORT, 'DB_NAME': DATA_DB_NAME})
AuthenticationCls = Authentication({'DB_HOST': DB_HOST, 'DB_PORT': DB_PORT, 'DB_NAME': AUTH_DB_NAME})

# FILTERS
AdminsFilter = Filters.user(ROOT)
for adminID in ADMINS:
    AdminsFilter |= Filters.user(adminID)

# AUXILIARY VARS
CHALLENGE, NEW_CHALLENGE, PVP = range(3)

# LOGGING
logger = LogHandler()

# GLOSSARY
Glossary = {
    'exit': 'Exit',
    'new_challenge':  'New challenge',
    'no_challenges':  'No challenges, create a new one',
    'challenge_list': 'Challenge list. Choose one by number or create new',
    'challenge_name': 'Write challenge name',
    'selected_challenge': 'Selected challenge:\n',
    'see_you': 'See you!',
    'challenge_created': 'Challenge created:\n',
    'challenge_wrong': 'Wrong challenge name',
}


def error(update: Update, context: CallbackContext):
    logger.error(context.error)


@handle_errors
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Congratulations, you're in the Choosen group!",
        reply_markup=ReplyKeyboardRemove())


@handle_errors
def challenge(update: Update, context: CallbackContext):
    context.user_data.clear()
    challenges = ChallengeCls.get_challenges()
    if challenges:
        menu = ReplyKeyboardMarkup(
            [[f"{Glossary['new_challenge']}"]]+\
            [[ch['name']] for ch in challenges],
            resize_keyboard=True)
        update.message.reply_text(
            f"{Glossary['challenge_list']}",
            reply_markup=menu)
    else:
        menu = ReplyKeyboardMarkup(
            [[f"{Glossary['new_challenge']}"]],
            resize_keyboard=True)
        update.message.reply_text(
            f"{Glossary['no_challenges']}",
            reply_markup=menu)

    return CHALLENGE


@handle_errors
def new_challenge(update: Update, context: CallbackContext):
    menu = ReplyKeyboardMarkup(
        [[f"{Glossary['exit']}"]],
        resize_keyboard=True)
    update.message.reply_text(
        f"{Glossary['challenge_name']}",
        reply_markup=menu)

    return NEW_CHALLENGE


@handle_errors
def choose_challenge(update: Update, context: CallbackContext):
    menu = ReplyKeyboardMarkup(
        [[f"{Glossary['exit']}"]],
        resize_keyboard=True)
    name = update.message.text
    if not ChallengeCls.get_challenge(name):
        update.message.reply_text(
            f"{Glossary['challenge_wrong']}{name}")
        return 

    context.user_data['challenge'] = name
    update.message.reply_text(
        f"{Glossary['selected_challenge']}{name}",
        reply_markup=menu)

    return ConversationHandler.END


@handle_errors
def create_challenge(update: Update, context: CallbackContext):
    menu = ReplyKeyboardMarkup(
        [[f"{Glossary['exit']}"]],
        resize_keyboard=True)
    name = update.message.text
    result = ChallengeCls.create(name)

    context.user_data['challenge'] = name
    update.message.reply_text(
        f"{Glossary['challenge_created']}{name}",
        reply_markup=menu)

    return ConversationHandler.END


@handle_errors
def done(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"{Glossary['see_you']}",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


AdminConversationHandler = ConversationHandler(
    entry_points=[
        CommandHandler('start', echo, filters=AdminsFilter),
        CommandHandler('challenge', challenge, filters=AdminsFilter),
    ],
    states={
        CHALLENGE: [
            MessageHandler(Filters.regex(f"^{Glossary['new_challenge']}$"), new_challenge),
            MessageHandler(Filters.text, choose_challenge),
        ],

        NEW_CHALLENGE: [
            MessageHandler(Filters.text, create_challenge),
        ],

        PVP: [
            # MessageHandler(Filters.regex('^Любимые...$'), favourites_choice),
            # MessageHandler(Filters.regex('^(Идеальный подарок - это|'
            #                              'Как предпочитаю проводить время)$'),
            #                regular_choice),
            # MessageHandler(Filters.regex('^До встречи!$'), done),
        ],
    },
    fallbacks=[
        MessageHandler(Filters.regex(f"^{Glossary['exit']}$"), done)
    ],
    per_chat=True,
)
