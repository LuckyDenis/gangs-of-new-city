# coding: utf8
from logging import getLogger

from aiogram import Dispatcher
from aiogram import Bot
from aiogram import types as t
from app.helpers import Cmds
from app import core


bot = Bot(
    token="",
    proxy="",
    parse_mode=t.ParseMode.HTML
)

logger = getLogger(__name__)
dp = Dispatcher(bot)


# ----- cmd: start ----- #
@dp.message_handler(commands=[Cmds.START])
async def cmd_start(message: t.Message):
    data = {
        "id": message.chat.id
    }
    train = core.NewUserTrain(data)
    await train.move()
    result = train.get_result()
    await publish_answers(message, result)


# ----- publish answer ----- #
async def publish_answers(message, result):
    answers = result["answers"]
    for answer in answers:
        await bot.send_message(
            message.chat.id,
            answer
        )
