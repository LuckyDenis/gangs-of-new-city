# coding: utf8
from logging import getLogger


from aiogram import types as t
from app.helpers import Cmds
from app import core
from app.views import Types

from app.configuration.settings import Setup
from aiogram import Dispatcher
from aiogram import Bot
from aiogram.types import ParseMode
from app.middlewares.storage import GinoMiddleware
from app.middlewares.unique_id import UniqueIdMiddleware
from app.views.emoji import emojize

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cfg")
args = parser.parse_args()

setup = Setup(path=args.cfg)


bot = Bot(
    token=setup.bot["token"],
    parse_mode=ParseMode.HTML
)
dp = Dispatcher(bot)
dp.middleware.setup(GinoMiddleware(setup.database))
dp.middleware.setup(UniqueIdMiddleware())


logger = getLogger(__name__)


# ----- cmd: start ----- #
@dp.message_handler(commands=[str(Cmds.START)])
async def cmd_start(message: t.Message, unique_id):
    data = {
        "is_bot": message.from_user.is_bot,
        "unique_id": unique_id,
        "id": message.chat.id,
        "language": message.from_user.language_code,
        "datetime": message.date.date(),
        "referral_id": message.get_args() or False
    }
    train = core.NewUserItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: ano ----- #
@dp.message_handler(regexp=f"^{emojize(':warning:')}")
@dp.message_handler(commands=[str(Cmds.ANO)])
async def cmd_ano(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date.date(),
    }
    train = core.UserIsNotAgreeItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: ayes ----- #
@dp.message_handler(regexp=f"^{emojize(':white_check_mark:')}")
@dp.message_handler(commands=[str(Cmds.AYES)])
async def cmd_ayes(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date.date(),
    }
    train = core.UserIsAgreeItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


async def done(answers):
    for answer in answers:
        send_handler = send_handlers(
            answer["message_type"]
        )
        await send_handler(answer)


def send_handlers(message_type):
    functions = {
        Types.TEXT_MESSAGE: send_text_message
    }
    return functions[message_type]


async def send_text_message(answer):
    await bot.send_message(
        answer["chat_id"],
        answer["text"],
        reply_markup=answer.get("keyboard")
    )
