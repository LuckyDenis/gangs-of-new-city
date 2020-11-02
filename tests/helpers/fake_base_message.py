# coding: utf8


class FakeMessage:
    @staticmethod
    def get_template(*_, **__):
        return "foobar"
