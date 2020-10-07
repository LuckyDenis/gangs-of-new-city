# coding: utf8

import errno
import sys
import functools

from python_json_config import ConfigBuilder


def singleton(cls):
    instance = None

    @functools.wraps(cls)
    def inner(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance
    return inner


builder = ConfigBuilder()


# ----- logging ----- #
builder.validate_field_type("logging.version", int)
builder.validate_field_type("logging.disable_existing_loggers", bool)

# ----- database ----- #
builder.validate_field_type("database.version", int)
builder.validate_field_type("database.connect.engine", str)
builder.validate_field_type("database.connect.port", int)
builder.validate_field_type("database.connect.host", str)
builder.validate_field_type("database.connect.login", str)
builder.validate_field_type("database.connect.password", str)
builder.validate_field_type("database.connect.name", str)
builder.validate_field_type("database.pool.min", int)
builder.validate_field_type("database.pool.max", int)

# ----- bot ----- #
builder.validate_field_type("bot.version", int)
builder.validate_field_type("bot.skip_update", bool)
builder.validate_field_type("bot.token", str)
builder.validate_field_type("bot.polling", bool)
builder.validate_field_type("bot.webhook.host", str)
builder.validate_field_type("bot.webhook.port", int)
builder.validate_field_type("bot.webhook.path", str)


# ----- Конфиг ----- #
@singleton
class Setup:
    def __init__(self, path):
        self._data = None
        self._path = path
        self._read()

    def _read(self):
        try:
            self._data = builder.parse_config(self._path)
        except (OSError, TypeError) as err:
            print(err)
            sys.exit(errno.EPERM)

    @property
    def logging(self):
        return self._data.logging.to_dict()

    @property
    def database(self):
        return self._data.database.to_dict()

    @property
    def bot(self):
        return self._data.bot.to_dict()
