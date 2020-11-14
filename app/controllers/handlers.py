# coding: utf8
from logging import getLogger


from aiogram import types as t
from app import core
from app.views import Types

from app.configuration.settings import Setup
from aiogram import Dispatcher
from aiogram import Bot
from aiogram.types import ParseMode
from app.middlewares.storage import GinoMiddleware
from app.middlewares.unique_id import UniqueIdMiddleware
from app.views import Cmds
from app.views import ECmds


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
@dp.message_handler(commands=Cmds.START.get())
async def cmd_start(message: t.Message, unique_id):
    data = {
        "is_bot": message.from_user.is_bot,
        "unique_id": unique_id,
        "id": message.chat.id,
        "language": message.from_user.language_code,
        "datetime": message.date,
        "referral_id": message.get_args() or False
    }
    train = core.UserStartItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: fnotaccept ----- #
@dp.message_handler(regexp=ECmds.FNOTACCEPT.get())
@dp.message_handler(commands=Cmds.FNOTACCEPT.get())
async def cmd_ano(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date,
    }
    train = core.NewUserIsNotAcceptItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: faccept ----- #
@dp.message_handler(regexp=ECmds.FACCEPT.get())
@dp.message_handler(commands=Cmds.FACCEPT.get())
async def cmd_ayes(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date,
    }
    train = core.NewUserIsAcceptItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: fen ----- #
@dp.message_handler(commands=Cmds.FEN.get())
async def cmd_ayes(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date,
    }
    train = core.NewUserPickEnLanguageItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: fru ----- #
@dp.message_handler(commands=Cmds.FRU.get())
async def cmd_ayes(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date,
    }
    train = core.NewUserPickRuLanguageItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: hname ----- #
@dp.message_handler(commands=Cmds.HNAME.get())
async def cmd_hname(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date,
        "hero_nick": message.get_args()
    }

    train = core.NewHeroItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: lang ----- #
@dp.message_handler(regexp=ECmds.LANG.get())
@dp.message_handler(commands=Cmds.LANG.get())
async def cmd_lang(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date,
    }

    train = core.ViewLanguagesItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- cmd: inn ----- #
@dp.message_handler(regexp=ECmds.INN.get())
@dp.message_handler(commands=Cmds.INN.get())
async def cmd_lang(message: t.Message, unique_id):
    data = {
        "unique_id": unique_id,
        "id": message.chat.id,
        "datetime": message.date,
    }

    train = core.ViewLanguagesItinerary(data)
    await train.move()
    answers = train.get_answers()
    await done(answers)


# ----- staff ----- #
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
