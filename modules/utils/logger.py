import logging
import coloredlogs
import logging.config


class LogHandler(logging.Logger):
    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it

        coloredlogs.DEFAULT_FIELD_STYLES = {
            'asctime': {'color': 'blue'},
            'hostname': {'color': 'magenta'},
            'levelname': {'color': 'black', 'bold': True},
            'name': {'color': 'blue'},
            'threadName': {'color': 'red'},
            'programname': {'color': 'cyan'}
        }

        coloredlogs.DEFAULT_LEVEL_STYLES = {
            'info': {'color': 'black'},
            'critical': {'color': 'red', 'bold': True},
            'error': {'color': 'red'},
            'debug': {'color': 'yellow'},
            'warning': {'color': 'cyan'}
        }

        logging_config = {
            'version': 1,
            'formatters': {
                'stream': {
                    '()': 'coloredlogs.ColoredFormatter',
                    'format': 'totalizator-bot: %(asctime)s  %(levelname)-5s %(processName)-11s'
                              '  %(threadName)-10s  %(message).1000s'
                }
            },
            'handlers': {
                'stream': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'stream',
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['stream'],
            },
        }
        logging.config.dictConfig(logging_config)
        cls.__it__ = it = logging.getLogger()
        return it
