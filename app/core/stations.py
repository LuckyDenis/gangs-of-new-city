# coding: utf8
"""
Использования подходов маленьких классов
содержащих какую-то одну логику упрощает
поддержку и повторное использования кода.

Например для вывода данных информации о
состоянии кошелька персонажа используется
класс `GetWalletSt` и этот же класс можно
переиспользовать для операции купли/продажи.
Принцип SOLID.

Записываем данные в словарь `queries`, для
централизованного хранения информации о запросах
и данных с которыми работает база данных.
"""
from logging import getLogger

import app.database as db
from .statuses import Statuses as Code
from app.views import answers as an
from re import fullmatch
logger = getLogger("stations")


class BaseSt:
    def __init__(self, train):
        self.train = train
        train.progress = {
            "name": self._station_name(),
            "status": True
        }
        logger.debug(self.train.payload)

    def _station_name(self):
        return self.__class__.__name__

    @property
    def exception(self):
        return self.train.exception

    @exception.setter
    def exception(self, err):
        self.train.exception = err

    @property
    def answers(self):
        return self.train.answers

    @answers.setter
    def answers(self, answer):
        self.train.answers = answer

    @answers.deleter
    def answers(self):
        del self.train.answers

    async def add_exception_answer(self):
        """
        Если в ходе выполнения запроса к базе мы получили ошибку,
        то все полученные до этого ответы в `train.answers` будут
        удаленны и добавлен ответ об ошибке. В реализации метода
        `BaseSt._traveled` нужно сделать проверку на ошибку явно.
        """

        del self.train.answers
        state = {
            "id": self.train.data["id"],
            "unique_id": self.train.data["unique_id"]
        }
        self.answers = await an.SystemException.get(state)

    async def traveled(self):
        """
        Работу с ошибками проводим тут, для инкапсуляции логики
        в одном месте и оставить чистой логику других объектов.
        :return: Bool
        """

        is_ok = False
        try:
            is_ok = await self._traveled()
        except KeyError:
            await self.add_exception_answer()
        return is_ok

    async def _traveled(self):
        """
        Тут в поражденных станция пишем логику работы.
        :return: Bool
        """
        raise NotImplementedError

    async def execution(self, storage_query, query_name):
        """
        Передаем в эту функцию парамметры, а не вызываем
        абстрактные методы, для сохранения гибкости классов.
        Возможна ситуация, когда нам потребуется в одном классе
        выполнить два запроса к базе данных.

        :param storage_query: передаем функцию,
            которая при вызове выполнит запрос к базе данных
        :param query_name: имя запроса, по которому можно
            найти запрос в train.queries
        :return: возращаем словарь, в котором данные от базы
            или пустой в случае неудачи.
        """
        result = {}
        try:
            result = await storage_query(
                self.train.queries[query_name])
        except Exception as e:
            self.exception = {"args": e.args, "traceback": e.__traceback__}
            await self.add_exception_answer()

        return result


class StartRailwayDepotSt(BaseSt):
    """
    Класс служит для обозначения начала пути,
    что бы не было, не очевидного добавления статуса
    `code.statuses.Statuses.IN_THE_WAY`. Наличие статуса
    необходимо для проверки коректности прохождения станций.
    Это требование `core.dispatcher.BaseItinerary.move`.
    todo:
    В этот класс можно встроить старт метрики `timeit`.
    """
    async def _traveled(self):
        return Code.IS_OK


class FinishRailwayDepotSt(BaseSt):
    """
    Класс служит для обозначения конца пути,
    todo:
    В этот класс можно встроить финиш метрики `timeit`.
    """
    async def _traveled(self):
        return Code.IS_OK


class GetUserSt(BaseSt):
    """
    Получаем пользователя или пустой словарь.

    Контракт:
    Обязательные данные: ['data']['id']
    Добавленные данные: ['states']['user']
    """
    def query_data(self):
        query_name = "get_user"
        self.train.queries[query_name] = {
            "id": self.train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.get

    async def _traveled(self):
        user = await self.execution(
            self.storage_query(), self.query_data())
        self.train.states["user"] = user

        if self.exception:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class UserTimeVisitedUpdateSt(BaseSt):
    def query_data(self):
        query_name = "user_time_visited_update"
        self.train.queries[query_name] = {
            "id": self.train.data["id"],
            "visited": self.train.data["datetime"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.user_time_visited_update

    async def _traveled(self):
        await self.execution(
            self.storage_query(), self.query_data())

        if self.exception:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsNewUserSt(BaseSt):
    """
    Проверка, что пользователь новый.

    Если пользователь обнаружен, добавляем ответ в список answers
    и уходим с маршрута.

    Контракт:
    Обязательные данные: ['states']['user']
    Добавленные данные: ['answers']['answer'] или None
    """
    async def add_out_answer(self):
        state = {
            "id": self.train.data["id"],
            "language": self.train.data["language"]
        }
        self.answers = await an.UserIsNotNew.get(state)

    async def _traveled(self):
        user = self.train.states['user']
        if user:  # Пользователь существует
            await self.add_out_answer()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class UserCreateSt(BaseSt):
    """
    Создаем нового пользователя.

    Контракт:
    Обязательные данные:
        ['data']['id']
        ['data']['language']
        ['data']['datetime']
    Добавленные данные: ['states']['user']
    """
    async def add_out_answer(self):
        state = {
            "id": self.train.data["id"],
            "language": self.train.data["language"]
        }
        self.train.answers = await an.NewUser.get(state)

    def query_data(self):
        query_name = "create_user"
        self.train.queries[query_name] = {
            "id": self.train.data["id"],
            "is_bot": self.train.data["is_bot"],
            "language": self.train.data["language"],
            "visited": self.train.data["datetime"],
            "registered": self.train.data["datetime"],
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.create

    async def _traveled(self):
        user = await self.execution(
            self.storage_query(), self.query_data())
        self.train.states["user"] = user

        if self.exception:
            return Code.EMERGENCY_STOP

        await self.add_out_answer()
        return Code.IS_OK


class DoesUserHaveReferralIdSt(BaseSt):
    """
    Проверка наличия пригласившиего пользователя.

    Если такого пользователя нет, то дальше
    идти нет смысла. Для отсутсвующего пользователя
    передовать аргумент None.

    Контракт:
    Обезателные данные: ['data']['referral_id']
    Дабавленные данные: None
    """
    async def _traveled(self):
        referral_id = self.train.data.get("referral_id")
        if not referral_id:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class GetInviterSt(BaseSt):
    """
    Берем пригласившего пользователя из базы данных.

    Делаем это для того, что бы убедиться, что пригла
    сивший пользователь существует.

    Контракт:
    Обезательные данные: ['data']['referral_id']
    Добавленные данные: ['states']['inviter']
    """
    def query_data(self):
        query_name = "get_inviter"
        self.train.queries[query_name] = {
            "id": self.train.data["referral_id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.get

    async def _traveled(self):
        inviter = await self.execution(
            self.storage_query(), self.query_data())
        self.train.states["inviter"] = inviter

        if self.exception:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsThereInviterSt(BaseSt):
    """
    Проверяем что нашли приглашающего в базе данных.

    Контракт:
    Обезательные данные: ['states']['inviter']
    Добавленные данные: None
    """
    async def _traveled(self):
        inviter = self.train.states["inviter"]
        if not inviter:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class UserIsInviterSt(BaseSt):
    """
    Пользователь не может сам себя пригласить.

    Контракт:
    Обезательные данные:
        ['states']['user']
        ['states']['inviter']
    Добавленные данные: None
    todo:
    Подумать, может ли возникнуть така ситуация.
    """
    async def _traveled(self):
        user = self.train.states['user']
        inviter = self.train.states['inviter']
        if user["id"] == inviter["id"]:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class AddReferralDataSt(BaseSt):
    """
    Добавляем информацию для будущего начисления бонуса.

    Контракт:
    Обезаетельные данные:
        ['data']['id']
        ['states']['inviter']['id']
    Добавленные данные: ['answers']['answer']
    """
    async def add_out_answers(self):
        self.train.answers = "сообщаем что дан боннус"

    def query_data(self):
        query_name = "add_referral_data"
        self.train.queries[query_name] = {
            'invited': self.train.data["id"],
            'inviter': self.train.states["inviter"]["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Referral.create

    async def _traveled(self):
        await self.execution(
            self.storage_query(), self.query_data()
        )

        if self.exception:
            return Code.EMERGENCY_STOP

        await self.add_out_answers()
        return Code.IS_OK


class IsThereUserSt(BaseSt):
    """
    Проверка, что пользователя нет в базе.

    Если пользователь не обнаружен, добавляем ответ в список answers
    и уходим с маршрута.

    Контракт:
    Обязательные данные: ['states']['user']
    Добавленные данные: ['answers']['answer'] или None
    """
    async def add_out_answer(self):
        state = {
            "id": self.train.data["id"]
        }
        self.answers = await an.UserIsNotFound.get(state)

    async def _traveled(self):
        user = self.train.states['user']
        if not user:  # Пользователь не существует
            await self.add_out_answer()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsUserBlockedSt(BaseSt):
    """
    Проверяем права на доступ к приложению.

    Контракт:
    Обязательные данные: ['states']['user']['is_blocked']
    Добавленные данные: ['answers']['answer'] или None
    """
    async def add_out_answer(self):
        self.answers = "Пользователь заблокирован"

    async def _traveled(self):
        user = self.train.states["user"]
        if user and user["is_blocked"]:
            await self.add_out_answer()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsCorrectHeroNickSt(BaseSt):
    """
    Проверка имени героя на корректность.

    Имя может содержать: a-z, A-Z, 0-9, точку,
    нижнее подчеркивание.
    """

    async def add_out_answer(self):
        state = {
            "id": self.train.data["id"],
            "language": self.train.states["user"]["language"]
        }
        self.answers = await an.HeroNickIsNotCorrect.get(state)

    async def _traveled(self):
        hero_nick = self.train.data["hero_nick"]

        if not fullmatch(r"^[A-Za-z0-9_.]{5,20}$", hero_nick):
            await self.add_out_answer()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class GetHeroSt(BaseSt):
    """
    Получение героя персонажа.

    Контракт:
    Обезательные данные: ['data']['id']
    Добавленные данные: ['states']['hero']
    """
    def query_data(self):
        query_name = "get_hero"
        self.train.queries[query_name] = {
            "id": self.train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Hero.get

    async def _traveled(self):
        hero = await self.execution(
            self.storage_query(), self.query_data()
        )
        self.train.states["hero"] = hero

        if self.exception:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsNewHeroSt(BaseSt):
    """
    Проверка на то, имеет ли пользователь уже героя.

    Контракт:
    Обезательные данные: ['states']['hero']
    Добавленные данные: ['answers']['answer'] или None
    """

    async def add_out_answers(self):
        self.train.answers = "у вас уже есть герой"

    async def _traveled(self):
        hero = self.train.states["user"]['is_hero']
        if hero:
            await self.add_out_answers()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class DoesUserHaveAgreeingSt(BaseSt):
    """
    Пользователь разрешил обработку персональных данных.

    Обезательные данные: ['states']['user']["is_agreeing']
    Добавленные данные: ['answers']['answer'] или None
    """
    async def add_out_answer(self):
        state = {
            "id": self.train.data["id"],
            "language": self.train.states["user"]["language"]
        }
        self.train.answers = await an.DoesUserHaveAgreeing.get(state)

    async def _traveled(self):
        is_agreeing = self.train.states["user"]["is_agreeing"]
        if not is_agreeing:
            await self.add_out_answer()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsNewHeroUniqueSt(BaseSt):
    """
    Проверка уникальности имени героя (имеет ли, кто-то еще
    героя с таким же именем).

    Контракт:
    Обезательные данные: ['data']['hero_nick']
    Добавленные данные: ['states']['is_hero']

    todo:
    Подумать: Надо разивать на два класса или это
    все таки одно логическое действие.
    """
    async def add_out_answers(self):
        self.train.answers = "не уникальное имя персонажа"

    def query_data(self):
        query_name = "check_hero_unique"
        self.train.queries[query_name] = {
            "hero_nick": self.train.data["hero_nick"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Hero.get_by_nick

    async def _traveled(self):
        is_hero = await self.execution(
            self.storage_query(), self.query_data()
        )
        self.train.states["is_hero"] = is_hero

        if self.exception:
            return Code.EMERGENCY_STOP

        if is_hero:
            await self.add_out_answers()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class NewHeroCreateSt(BaseSt):
    """
    Создаем нового героя.

    Контракт:
    Обезательные данные:
        ['data']['id']
        ['data']['hero_nick']
    Добавленные данные:
        ['states']['new_hero']
        ['answers']['answer']
    """
    async def add_out_answers(self):
        self.train.answers = "создан новый герой"

    def query_data(self):
        query_name = "create_new_hero"
        self.train.queries[query_name] = {
            "id": self.train.data["id"],
            "hero_nick": self.train.data["hero_nick"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Hero.create

    async def _traveled(self):
        new_hero = await self.execution(
            self.storage_query(), self.query_data()
        )
        self.train.states['new_hero'] = new_hero

        if self.exception:
            return Code.EMERGENCY_STOP

        await self.add_out_answers()
        return Code.IS_OK


class GetWalletSt(BaseSt):
    """
    Получения информаци о кошельке героя.

    Контракт:
    Обезаетльные данные: ['data']['id']
    Добавленные данные: ['states']['wallet']
    """
    def query_data(self):
        query_name = "get_wallet"
        self.train.queries[query_name] = {
            "id": self.train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Wallet.get

    async def _traveled(self):
        wallet = await self.execution(
            self.storage_query(), self.query_data()
        )
        self.train.states["wallet"] = wallet

        if self.exception:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsThereWalletSt(BaseSt):
    """
    Отвечает за проверку существование кошелька героя в базе данных.
    Если кошелька нет, подразумевается, что герой еще не создан.

    Контракт:
    Обезаетельные данные: ['states']['wallet']
    Добавленные данные: ['answers']['answer'] или None
    """
    async def add_out_answers(self):
        self.train.answers = "Создайте героя"

    async def _traveled(self):
        wallet = self.train.states["wallet"]
        if not wallet:
            await self.add_out_answers()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class ViewWalletSt(BaseSt):
    """
    Отвечает за получение отрендеренного ответа для вывода информации
    о кошельке героя.

    Контракт:
    Обезаетельные данные: ['states']['wallet']
    Добавленные данные: ['answers']['answer']
    """
    async def add_out_answers(self):
        self.train.answers = "кошелек игрока"

    async def _traveled(self):
        await self.add_out_answers()
        return Code.IS_OK


class IsThereHeroSt(BaseSt):
    """
    Отвечает за проверку существование героя в базе данных.
    Если героя нет, подразумевается, что он еще не создан.

    Контракт:
    Обезаетельные данные: ['states']['hero']
    Добавленные данные: ['answers']['answer'] или None
    """
    async def add_out_answers(self):
        self.train.answers = "Создайте героя"

    async def _traveled(self):
        hero = self.train.states["hero"]
        if not hero:
            await self.add_out_answers()
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class ViewHeroSt(BaseSt):
    """
    Отвечает за получение отрендеренного ответа для вывода информации
    о герое.

    Контракт:
    Обезаетельные данные: ['states']['hero']
    Добавленные данные: ['answers']['answer']
    """
    async def add_out_answers(self):
        self.train.answers = "Информация об герои игрока"

    async def _traveled(self):
        await self.add_out_answers()
        return Code.IS_OK


class UserIsNotAgreeSt(BaseSt):
    async def add_out_answers(self):
        state = {
            "id": self.train.data["id"],
            "language": self.train.states["user"]["language"]
        }
        self.train.answers = await an.UserIsNotAgree.get(state)

    def query_data(self):
        query_name = "is_not_agree"
        self.train.queries[query_name] = {
            "id": self.train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.is_not_agree_policy

    async def _traveled(self):
        await self.execution(
            self.storage_query(), self.query_data()
        )
        if self.exception:
            return Code.EMERGENCY_STOP

        await self.add_out_answers()
        return Code.IS_OK


class UserIsAgreeHintSt(BaseSt):
    async def add_out_answers(self):
        state = {
            "id": self.train.data["id"],
            "language": self.train.states["user"]["language"]
        }
        self.train.answers = await an.UserIsAgreeHint.get(state)

    async def _traveled(self):
        is_hint = self.train.states["user"]["is_hint"]
        if not is_hint:
            return Code.IS_OK

        await self.add_out_answers()
        return Code.IS_OK


class UserIsAgreeSt(BaseSt):
    async def add_out_answers(self):
        state = {
            "id": self.train.data["id"],
            "language": self.train.states["user"]["language"]
        }
        self.train.answers = await an.UserIsAgree.get(state)

    def query_data(self):
        query_name = "is_agree"
        self.train.queries[query_name] = {
            "id": self.train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.is_agree_policy

    async def _traveled(self):
        await self.execution(
            self.storage_query(), self.query_data()
        )

        if self.exception:
            return Code.EMERGENCY_STOP

        await self.add_out_answers()
        return Code.IS_OK


class ViewLanguagesSt(BaseSt):
    async def add_out_answers(self):
        state = {
            "id": self.train.data["id"],
            "language": self.train.states["user"]["language"]
        }
        self.train.answers = await an.ViewLanguages.get(state)

    async def _traveled(self):
        await self.add_out_answers()
        return Code.IS_OK
