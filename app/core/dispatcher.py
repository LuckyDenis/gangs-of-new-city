# coding: utf8

from logging import getLogger
from pprint import pformat
from pprint import pp


from app.core import stations as st
from app.core.train import Train


logger = getLogger("dispatcher")


class BaseItinerary:
    def __init__(self, data):
        self.train = Train(data)
        self.data_has_required_keys()

    def add_checkpoint(self):
        for station in self.stations():
            self.train.progress = {
                "name": station.__name__,
                "status": False
            }

    async def move(self):
        """
        Перемещаемся от станции к станции, пока не дойдем
        до последней или не получим сообщение
        `core.statuses.EMERGENCE_STOP`. Входе движения
        получаем, обрабатываем, сохраняем данные для ответа
        пользователю.
        :return: None
        """
        self.add_checkpoint()
        for station in self.stations():
            is_ok = await station.traveled(self.train)
            pp(self.train.payload)
            if not is_ok:
                break
        logger.info(pformat(self.train.payload))

    def data_has_required_keys(self):
        for key in self.required_keys():
            if not self.train.data.get(key):
                return False
        return True

    def get_answers(self):
        return self.train.answers

    def stations(self):
        """
        Возращает список классов порожденных от класса
        `core.stations.BaseSt`. Используется для сбора и
        обработки информации сообщения пользователя.
        Подробней о мотивации в модуле `core.stations`.

        Паттерн: Цепочка обязанностей.
        :return: [BaseSt]
        """
        raise NotImplementedError

    def required_keys(self):
        """
        Список ключей которые должные быть обезательно
        во входном словаре `data`.
        :return: [str, int]
        todo:
        Подумать о том, являются ли данные которые
        передаются в класс доверительными в плане
        типов, если нет то добавить валидацию.
        Например: check_data = [
            {"key": "id", "type": int},
            {"key": "datetime", "type": datetime}
        ] или https://pypi.org/project/schema/
        """
        raise NotImplementedError


class UserStartItinerary(BaseItinerary):
    """
    cmd: /start

    :param data: {
        "id": user id,
        "language": database.fixture.Language,
        "datetime": datetime.datetime,
        "referral_id": referral id
    }
    """
    def required_keys(self):
        return ["id", "language", "datetime"]

    def stations(self):
        """
        Сначало создам пользователя, потом обработываем
        пригласившего.
        """
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsNewUserSt,
            st.UserCreateSt,
            st.DoesUserHaveReferralIdSt,
            st.GetInviterSt,
            st.IsThereInviterSt,
            st.UserIsInviterSt,
            st.AddReferralDataSt,
            st.FinishRailwayDepotSt
        ]


class NewUserIsNotAcceptItinerary(BaseItinerary):
    """
    cmd: /fnotaccept
    """
    def required_keys(self):
        return ["id"]

    def stations(self):
        """
        Пользователь отказался принять политику.
        """
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.IsUserBlockedSt,
            st.NewUserIsNotAcceptSt,
            st.FinishRailwayDepotSt
        ]


class NewUserIsAcceptItinerary(BaseItinerary):
    """
    cmd: /faccept
    """
    def required_keys(self):
        return ["id"]

    def stations(self):
        """
        Новый пользователь принял политику,
        показываем ему выбор языка.
        """
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.IsUserBlockedSt,
            st.UserIsAcceptSt,
            st.ViewNewUserIsAccept,
            st.FinishRailwayDepotSt
        ]


class UserIsAcceptItinerary(BaseItinerary):
    """
    cmd: /saccept
    """
    def required_keys(self):
        return ["id"]

    def stations(self):
        """
        Новый пользователь принял политику,
        показываем ему выбор языка.
        """
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.IsUserBlockedSt,
            st.UserIsAcceptSt,
            st.ViewUserIsAccept,
            st.FinishRailwayDepotSt
        ]


class NewUserPickEnLanguageItinerary(BaseItinerary):
    """
    cmd: /fen
    """
    def required_keys(self):
        return ["id"]

    def stations(self):
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.UserTimeVisitedUpdateSt,
            st.DoesUserRejectPolicySt,
            st.UserPickEnLanguage,
            st.CreateNewHeroHintSt,
            st.ViewCreateNewHeroSt,
            st.FinishRailwayDepotSt
        ]


class NewUserPickRuLanguageItinerary(BaseItinerary):
    """
    cmd: /fru
    """
    def required_keys(self):
        return ["id"]

    def stations(self):
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.UserTimeVisitedUpdateSt,
            st.DoesUserRejectPolicySt,
            st.UserPickRuLanguage,
            st.CreateNewHeroHintSt,
            st.ViewCreateNewHeroSt,
            st.FinishRailwayDepotSt
        ]


class ViewLanguagesItinerary(BaseItinerary):
    """
    cmd: /lang
    """
    def required_keys(self):
        return ["id", "datetime"]

    def stations(self):
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.UserTimeVisitedUpdateSt,
            st.DoesUserRejectPolicySt,
            st.ViewLanguagesSt,
            st.FinishRailwayDepotSt
        ]


class NewHeroItinerary(BaseItinerary):
    """
    cmd: /hname "hero"
    """
    def required_keys(self):
        return ["id", "hero_nick"]

    def stations(self):
        """
        Сначало проеверяем, имеет пользователь героя,
        потом проверяем уникальность ника героя.
        """
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.UserTimeVisitedUpdateSt,
            st.DoesUserRejectPolicySt,
            st.IsUserBlockedSt,
            st.IsCorrectHeroNickSt,
            st.IsNewHeroSt,
            st.IsNewHeroUniqueSt,
            st.NewHeroCreateSt,
            st.FinishRailwayDepotSt
        ]


class GetWalletItinerary(BaseItinerary):
    """
    cmd: /wallet
    """
    def required_keys(self):
        return ["id"]

    def stations(self):
        """
        Получаем информацию о кошельке, если кошелек
        не найден, то подразумеваем, что герой не создан.
        """
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.IsUserBlockedSt,
            st.IsThereHeroSt,
            st.GetWalletSt,
            st.ViewWalletSt,
            st.FinishRailwayDepotSt
        ]


class GetHeroItinerary(BaseItinerary):
    """
    cmd: /hero
    """
    def required_keys(self):
        return ["id"]

    def stations(self):
        return [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsThereUserSt,
            st.IsUserBlockedSt,
            st.IsThereHeroSt,
            st.GetHeroSt,
            st.ViewHeroSt,
            st.FinishRailwayDepotSt
        ]
