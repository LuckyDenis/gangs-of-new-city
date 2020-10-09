# coding: utf8
import gettext
import os
from babel.support import LazyProxy
from app.helpers import singleton
from contextvars import ContextVar
from app.database.fixture import Languages


@singleton
class I18N:
    ctx_locale = ContextVar(
        'ctx_user_locale', default=Languages.ENGLISH)

    def __init__(self, setup=None):
        setup = setup or {}
        self.path = setup.get("path")
        self.domain = setup.get("domain")
        self.locales = {}

    def set_setup(self, setup):
        self.path = setup.get("path")
        self.domain = setup.get("domain")
        self.reload()

    def reload(self):
        self.locales = self.find_locales()

    def set_locale(self, language):
        self.ctx_locale.set(language)

    def find_locales(self):
        translations = dict()

        for name in os.listdir(self.path):
            if not os.path.isdir(os.path.join(self.path, name)):
                continue
            mo_path = os.path.join(
                self.path, name, 'LC_MESSAGES', self.domain + '.mo')

            if os.path.exists(mo_path):
                with open(mo_path, "rb") as fp:
                    translations[name] = gettext.GNUTranslations(fp)
            elif os.path.exists(mo_path[:-2] + "po"):
                raise RuntimeError(f"Found locale '{name} "
                                   f"but this language "
                                   f"is not compiled!")

        return translations

    def gettext(self, singular, plural=None, n=1, locale=None):
        if locale is None:
            locale = self.ctx_locale.get()

        if locale not in set(self.locales):
            if n == 1:
                return singular
            return plural

        translator = self.locales[locale]

        if plural is None:
            return translator.gettext(singular)
        return translator.ngettext(singular, plural, n)

    def gettext_lazy(
            self, singular, plural=None, n=1,
            locale=None, enable_cache=True):
        return LazyProxy(
            self.gettext, singular, plural, n,
            locale, enable_cache=enable_cache)

    def __call__(self, singular, plural=None, n=1, locale=None):
        return self.gettext(singular, plural, n, locale)
