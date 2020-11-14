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
    @classmethod
    def add_exception_answer(cls, train):
        """
        Если в ходе выполнения запроса к базе мы получили ошибку,
        то все полученные до этого ответы в `train.answers` будут
        удаленны и добавлен ответ об ошибке. В реализации метода
        `BaseSt._traveled` нужно сделать проверку на ошибку явно.
        """

        del train.answers
        state = {
            "id": train.data["id"],
            "unique_id": train.data["unique_id"]
        }
        train.answers = an.SystemException.get(state)

    @classmethod
    def mark_checkpoint(cls, train):
        train.progress = {
            "name": cls.__name__,
            "status": True
        }
        logger.debug(train.payload)

    @classmethod
    async def traveled(cls, train):
        """
        Работу с ошибками проводим тут, для инкапсуляции логики
        в одном месте и оставить чистой логику других объектов.
        :return: Bool
        """
        cls.mark_checkpoint(train)
        is_ok = False
        try:
            is_ok = await cls._traveled(train)
        except KeyError:
            cls.add_exception_answer(train)
        return is_ok

    @classmethod
    async def _traveled(cls, train):
        """
        Тут в поражденных станция пишем логику работы.
        :return: Bool
        """
        raise NotImplementedError

    @classmethod
    async def execution(cls, train, storage_query, query_name):
        """
        Передаем в эту функцию парамметры, а не вызываем
        абстрактные методы, для сохранения гибкости классов.
        Возможна ситуация, когда нам потребуется в одном классе
        выполнить два запроса к базе данных.

        :param train:
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
                train.queries[query_name])
        except Exception as e:
            train.exception = {"args": e.args, "traceback": e.__traceback__}
            cls.add_exception_answer(train)

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
    @classmethod
    async def _traveled(cls, train):
        return Code.IS_OK


class FinishRailwayDepotSt(BaseSt):
    """
    Класс служит для обозначения конца пути,
    todo:
    В этот класс можно встроить финиш метрики `timeit`.
    """
    @classmethod
    async def _traveled(cls, train):
        return Code.IS_OK


class GetUserSt(BaseSt):
    """
    Получаем пользователя или пустой словарь.

    Контракт:
    Обязательные данные: ['data']['id']
    Добавленные данные: ['states']['user']
    """
    @classmethod
    def query_data(cls, train):
        query_name = "get_user"
        train.queries[query_name] = {
            "id": train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.get

    @classmethod
    async def _traveled(cls, train):
        user = await cls.execution(
            train, cls.storage_query(), cls.query_data(train))
        train.states["user"] = user

        if train.exception:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class UserTimeVisitedUpdateSt(BaseSt):
    @classmethod
    def query_data(cls, train):
        query_name = "user_time_visited_update"
        train.queries[query_name] = {
            "id": train.data["id"],
            "visited": train.data["datetime"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.user_time_visited_update

    @classmethod
    async def _traveled(cls, train):
        await cls.execution(
            train, cls.storage_query(), cls.query_data(train))

        if train.exception:
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
    @classmethod
    def add_out_answer(cls, train):
        state = {
            "id": train.data["id"],
            "language": train.data["language"]
        }
        train.answers = an.UserIsNotNew.get(state)

    @classmethod
    async def _traveled(cls, train):
        user = train.states['user']
        if user:  # Пользователь существует
            cls.add_out_answer(train)
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
    @classmethod
    def add_out_answer(cls, train):
        state = {
            "id": train.data["id"],
            "language": train.data["language"]
        }
        train.answers = an.NewUser.get(state)

    @classmethod
    def query_data(cls, train):
        query_name = "create_user"
        train.queries[query_name] = {
            "id": train.data["id"],
            "is_bot": train.data["is_bot"],
            "language": train.data["language"],
            "visited": train.data["datetime"],
            "registered": train.data["datetime"],
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.create

    @classmethod
    async def _traveled(cls, train):
        user = await cls.execution(
            train, cls.storage_query(), cls.query_data(train))
        train.states["user"] = user

        if train.exception:
            return Code.EMERGENCY_STOP

        cls.add_out_answer(train)
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
    @classmethod
    async def _traveled(cls, train):
        referral_id = train.data.get("referral_id")
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
    @classmethod
    def query_data(cls, train):
        query_name = "get_inviter"
        train.queries[query_name] = {
            "id": train.data["referral_id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.get

    @classmethod
    async def _traveled(cls, train):
        inviter = await cls.execution(
            train, cls.storage_query(), cls.query_data(train))
        train.states["inviter"] = inviter

        if train.exception:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsThereInviterSt(BaseSt):
    """
    Проверяем что нашли приглашающего в базе данных.

    Контракт:
    Обезательные данные: ['states']['inviter']
    Добавленные данные: None
    """
    @classmethod
    async def _traveled(cls, train):
        inviter = train.states["inviter"]
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
    @classmethod
    async def _traveled(cls, train):
        user = train.states['user']
        inviter = train.states['inviter']
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
    @classmethod
    def add_out_answers(cls, train):
        train.answers = "сообщаем что дан боннус"

    @classmethod
    def query_data(cls, train):
        query_name = "add_referral_data"
        train.queries[query_name] = {
            'invited': train.data["id"],
            'inviter': train.states["inviter"]["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Referral.create

    @classmethod
    async def _traveled(cls, train):
        await cls.execution(
            train, cls.storage_query(), cls.query_data(train)
        )

        if train.exception:
            return Code.EMERGENCY_STOP

        cls.add_out_answers(train)
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
    @classmethod
    def add_out_answer(cls, train):
        state = {
            "id": train.data["id"]
        }
        train.answers = an.UserIsNotFound.get(state)

    @classmethod
    async def _traveled(cls, train):
        user = train.states['user']
        if not user:  # Пользователь не существует
            cls.add_out_answer(train)
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsUserBlockedSt(BaseSt):
    """
    Проверяем права на доступ к приложению.

    Контракт:
    Обязательные данные: ['states']['user']['is_blocked']
    Добавленные данные: ['answers']['answer'] или None
    """
    @classmethod
    def add_out_answer(cls, train):
        train.answers = "Пользователь заблокирован"

    @classmethod
    async def _traveled(cls, train):
        user = train.states["user"]
        if user and user["is_blocked"]:
            cls.add_out_answer(train)
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsCorrectHeroNickSt(BaseSt):
    """
    Проверка имени героя на корректность.

    Имя может содержать: a-z, A-Z, 0-9, точку,
    нижнее подчеркивание.
    """

    @classmethod
    def add_out_answer(cls, train):
        state = {
            "id": train.data["id"],
            "language": train.states["user"]["language"]
        }
        train.answers = an.HeroNickIsNotCorrect.get(state)

    @classmethod
    async def _traveled(cls, train):
        hero_nick = train.data["hero_nick"]

        if not fullmatch(r"^[A-Za-z0-9_.]{5,20}$", hero_nick):
            cls.add_out_answer(train)
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class GetHeroSt(BaseSt):
    """
    Получение героя персонажа.

    Контракт:
    Обезательные данные: ['data']['id']
    Добавленные данные: ['states']['hero']
    """
    @classmethod
    def query_data(cls, train):
        query_name = "get_hero"
        train.queries[query_name] = {
            "id": train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Hero.get

    @classmethod
    async def _traveled(cls, train):
        hero = await cls.execution(
            train, cls.storage_query(), cls.query_data(train)
        )
        train.states["hero"] = hero

        if train.exception:
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class IsNewHeroSt(BaseSt):
    """
    Проверка на то, имеет ли пользователь уже героя.

    Контракт:
    Обезательные данные: ['states']['hero']
    Добавленные данные: ['answers']['answer'] или None
    """

    @classmethod
    def add_out_answers(cls, train):
        train.answers = "у вас уже есть герой"

    @classmethod
    async def _traveled(cls, train):
        hero = train.states["user"]['is_hero']
        if hero:
            cls.add_out_answers(train)
            return Code.EMERGENCY_STOP

        return Code.IS_OK


class DoesUserHaveAgreeingSt(BaseSt):
    """
    Пользователь разрешил обработку персональных данных.

    Обезательные данные: ['states']['user']["is_agreeing']
    Добавленные данные: ['answers']['answer'] или None
    """
    @classmethod
    def add_out_answer(cls, train):
        state = {
            "id": train.data["id"],
            "language": train.states["user"]["language"]
        }
        train.answers = an.DoesUserHaveAgreeing.get(state)

    @classmethod
    async def _traveled(cls, train):
        is_agreeing = train.states["user"]["is_agreeing"]
        if not is_agreeing:
            cls.add_out_answer(train)
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
    @classmethod
    def add_out_answers(cls, train):
        train.answers = "не уникальное имя персонажа"

    @classmethod
    def query_data(cls, train):
        query_name = "is_nick_unique"
        train.queries[query_name] = {
            "hero_nick": train.data["hero_nick"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Hero.get_by_nick

    @classmethod
    async def _traveled(cls, train):
        is_nick_busy = await cls.execution(
            train, cls.storage_query(), cls.query_data(train)
        )
        train.states["is_nick_busy"] = is_nick_busy

        if train.exception:
            return Code.EMERGENCY_STOP

        if is_nick_busy:
            cls.add_out_answers(train)
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
    @classmethod
    def add_out_answers(cls, train):
        train.answers = "создан новый герой"

    @classmethod
    def query_data(cls, train):
        query_name = "create_new_hero"
        train.queries[query_name] = {
            "id": train.data["id"],
            "hero_nick": train.data["hero_nick"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Hero.create

    @classmethod
    async def _traveled(cls, train):
        new_hero = await cls.execution(
            train, cls.storage_query(), cls.query_data(train)
        )
        train.states['new_hero'] = new_hero

        if train.exception:
            return Code.EMERGENCY_STOP

        cls.add_out_answers(train)
        return Code.IS_OK


class GetWalletSt(BaseSt):
    """
    Получения информаци о кошельке героя.

    Контракт:
    Обезаетльные данные: ['data']['id']
    Добавленные данные: ['states']['wallet']
    """
    @classmethod
    def query_data(cls, train):
        query_name = "get_wallet"
        train.queries[query_name] = {
            "id": train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Wallet.get

    @classmethod
    async def _traveled(cls, train):
        wallet = await cls.execution(
            train, cls.storage_query(), cls.query_data(train)
        )
        train.states["wallet"] = wallet

        if train.exception:
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
    @classmethod
    def add_out_answers(cls, train):
        train.answers = "Создайте героя"

    @classmethod
    async def _traveled(cls, train):
        wallet = train.states["wallet"]
        if not wallet:
            cls.add_out_answers(train)
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
    @classmethod
    def add_out_answers(cls, train):
        train.answers = "кошелек игрока"

    @classmethod
    async def _traveled(cls, train):
        cls.add_out_answers(train)
        return Code.IS_OK


class IsThereHeroSt(BaseSt):
    """
    Отвечает за проверку существование героя в базе данных.
    Если героя нет, подразумевается, что он еще не создан.

    Контракт:
    Обезаетельные данные: ['states']['hero']
    Добавленные данные: ['answers']['answer'] или None
    """
    @classmethod
    def add_out_answers(cls, train):
        train.answers = "Создайте героя"

    @classmethod
    async def _traveled(cls, train):
        is_hero = train.states["user"]["is_hero"]
        if not is_hero:
            cls.add_out_answers(train)
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
    @classmethod
    def add_out_answers(cls, train):
        train.answers = "Информация об герои игрока"

    @classmethod
    async def _traveled(cls, train):
        cls.add_out_answers(train)
        return Code.IS_OK


class UserIsNotAgreeSt(BaseSt):
    @classmethod
    def add_out_answers(cls, train):
        state = {
            "id": train.data["id"],
            "language": train.states["user"]["language"]
        }
        train.answers = an.UserIsNotAgree.get(state)

    @classmethod
    def query_data(cls, train):
        query_name = "is_not_agree"
        train.queries[query_name] = {
            "id": train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.is_not_agree_policy

    @classmethod
    async def _traveled(cls, train):
        await cls.execution(
            train, cls.storage_query(), cls.query_data(train)
        )
        if train.exception:
            return Code.EMERGENCY_STOP

        cls.add_out_answers(train)
        return Code.IS_OK


class UserIsAgreeHintSt(BaseSt):
    @classmethod
    def add_out_answers(cls, train):
        state = {
            "id": train.data["id"],
            "language": train.states["user"]["language"]
        }
        train.answers = an.UserIsAgreeHint.get(state)

    @classmethod
    async def _traveled(cls, train):
        is_hint = train.states["user"]["is_hint"]
        if not is_hint:
            return Code.IS_OK

        cls.add_out_answers(train)
        return Code.IS_OK


class UserIsAgreeSt(BaseSt):
    @classmethod
    def add_out_answers(cls, train):
        state = {
            "id": train.data["id"],
            "language": train.states["user"]["language"]
        }
        train.answers = an.UserIsAgree.get(state)

    @classmethod
    def query_data(cls, train):
        query_name = "is_agree"
        train.queries[query_name] = {
            "id": train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.is_agree_policy

    @classmethod
    async def _traveled(cls, train):
        await cls.execution(
            train, cls.storage_query(), cls.query_data(train)
        )

        if train.exception:
            return Code.EMERGENCY_STOP

        cls.add_out_answers(train)
        return Code.IS_OK


class ViewLanguagesSt(BaseSt):
    @classmethod
    def add_out_answers(cls, train):
        state = {
            "id": train.data["id"],
            "language": train.states["user"]["language"]
        }
        train.answers = an.ViewLanguages.get(state)

    @classmethod
    async def _traveled(cls, train):
        cls.add_out_answers(train)
        return Code.IS_OK
