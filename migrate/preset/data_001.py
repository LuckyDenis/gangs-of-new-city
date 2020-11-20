# coding: utf8
"""
Данные необходимые для нормальной работы базы данных.
Подключить в первом файле миграции в папке `migrate.version`
в конце функции `upgrade`. Беспокоиться об откате данных не нужно
так как удаляться таблицы в которых данные храняться.
"""

from app.database.fixture import Languages
from app.database.fixture import Gangs
from app.database.models import Language
from app.database.models import Gang


def update_data(op):
    codes = [
        {"code": Languages.RUSSIAN},
        {"code": Languages.ENGLISH}
    ]
    colors = [
        {"color": Gangs.GREEN},
        {"color": Gangs.ORANGE}
    ]
    op.bulk_insert(Language, codes)
    op.bulk_insert(Gang, colors)
