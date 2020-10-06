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

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cfg")
args = parser.parse_args()

setup = Setup(args.cfg)


bot = Bot(
    token=setup.bot["token"],
    parse_mode=ParseMode.HTML
)
dp = Dispatcher(bot)

logger = getLogger(__name__)


# ----- cmd: start ----- #
@dp.message_handler(commands=[str(Cmds.START)])
async def cmd_start(message: t.Message):
    data = {
        "id": message.chat.id,
        "language": "en",
        "datetime": message.date.date(),
        "referral_id": message.get_args() or False
    }
    train = core.NewUserItinerary(data)
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
        answer["text"]
    )
