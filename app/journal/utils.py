# coding: utf8
import os
import shutil
from logging.handlers import RotatingFileHandler
import logging


def owned_rotating_file_handler(filename, mode='a', max_bytes=0,
                                backup_count=0, encoding=None, owner=None):
    if owner:
        if not os.path.exists(filename):
            open(filename, 'a').close()
        shutil.chown(filename, *owner)
    return RotatingFileHandler(filename, mode, max_bytes, backup_count, encoding)


def owned_file_handler(filename, mode='a', encoding=None, owner=None):
    if owner:
        if not os.path.exists(filename):
            open(filename, 'a').close()
        shutil.chown(filename, *owner)
    return logging.FileHandler(filename, mode, encoding)
