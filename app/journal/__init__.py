# coding: utf8
"""
Так как для настройки логгирования испозьются
`logging.config.dictConfig`. При таком методе, что бы использовать
классы порожденные от `FileHandler`, нужно в файле конфигурации
передовать ссылку на функцию, для работы с привелегиями,
которая будет вызвана в процессе настройки.

Пример:
{
 ...,
 "handlers": {
    "default": {
        "()": "ext://__main__.journal.owned_file_handler",
        ...
    }
}

И что бы не было конфликтов имен, пакет назван `journal`.
Так же для корректной работы, функции должны быть импортированны
в область видимости где происходит инцилизация логгера.

Подробнее: https://docs.python.org/3.6/library/logging.config.html#logging.config.dictConfig
"""

from logging import config
from .utils import owned_file_handler
from .utils import owned_rotating_file_handler


__all__ = [
    "config",
    "owned_file_handler",
    "owned_rotating_file_handler"
]
