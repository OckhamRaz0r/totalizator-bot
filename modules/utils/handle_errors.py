#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import \
    ConversationHandler
from .logger import LogHandler


# LOGGING
logger = LogHandler()


# ERROR HANDLING DECORATOR
def handle_errors(method):
    def error_wrapper(self, *args, **kwargs):
        result = ConversationHandler.END
        try:
            result = method(self, *args, **kwargs)
        except Exception as e:
            logger.error(e)
        return result
    return error_wrapper
