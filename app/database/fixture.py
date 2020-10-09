# coding: utf8


class Languages:
    RUSSIAN = "ru"
    ENGLISH = "en"

    @classmethod
    def has(cls, item):
        return item in vars(cls).values()

    @classmethod
    def for_user(cls, item):
        language = cls.ENGLISH  # по умолчанию
        if cls.has(item):
            language = item
        return language


class Gangs:
    RED = "red"
    YELLOW = "yellow"
    ORANGE = "orange"
