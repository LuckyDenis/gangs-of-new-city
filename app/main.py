# coding: utf8

from aiogram import executor
from app.controllers.handlers import setup
from app.controllers.handlers import dp
from app import journal
from app import views

from logging import getLogger


journal.config.dictConfig(setup.logging)
views.i18n.set_setup(setup.i18n)

logger = getLogger("app")


def main():
    executor.start_polling(
        dispatcher=dp,
        skip_updates=setup.bot["skip_updates"]
    )


if __name__ == '__main__':
    main()
