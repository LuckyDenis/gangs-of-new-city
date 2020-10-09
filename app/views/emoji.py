# coding: utf8
import emoji


def emojize(text):
    return emoji.emojize(str(text), use_aliases=True)


def demojize(text):
    return emoji.demojize(text)
