import os
import sys
import string

import cherrypy

from babel.support import Translations

from openobject.i18n.utils import get_locale


__all__ = ['get_translations', 'load_translations', 'gettext', 'install']


_translations = {}


def get_translations(locale, domain=None):

    domain = domain or "messages"

    cats = _translations.setdefault(domain, {})
    try:
        return cats[locale]
    except KeyError:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        load_translations(os.path.join(path, "locales"), [locale])
        return cats[locale]


def load_translations(path, locales=None, domain=None):

    domain = domain or "messages"
    catalog = _translations.setdefault(domain, {})

    if not locales:
        locales = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    if domain == "javascript":
        jspath = os.path.join(os.path.dirname(path), "static", "javascript", "i18n")

    for lang in locales:

        if domain == "messages":
            tr = Translations.load(path, [lang], domain)
            if isinstance(tr, Translations):
                if lang in catalog:
                    catalog[lang].merge(tr)
                else:
                    catalog[lang] = tr

        if domain == "javascript":
            fname = os.path.join(jspath, "%s.js" % lang)
            if os.path.exists(fname):
                _all = catalog.setdefault(lang, [])
                _all.append(fname)


def _gettext(key, locale=None, domain=None):
    """Get the gettext value for key.

    Added to builtins as '_'. Returns Unicode string.

    @param key: text to be translated
    @param locale: locale code to be used.
        If locale is None, gets the value provided by get_locale.

    """
    if locale is None:
        locale = get_locale()
    if key == '':
        return '' # special case
    try:
        return get_translations(locale, domain).ugettext(key)
    except KeyError:
        return key
    except IOError:
        return key

class lazystring(object):
    """Has a number of lazily evaluated functions replicating a string.

    Just override the eval() method to produce the actual value.

    """

    def __init__(self, func, *args, **kw):
        self.func = func
        self.args = args
        self.kw = kw

    def eval(self):
        return self.func(*self.args, **self.kw)

    def __unicode__(self):
        return unicode(self.eval())

    def __str__(self):
        return str(self.eval())

    def __mod__(self, other):
        return self.eval() % other

    def __cmp__(self, other):
        return cmp(self.eval(), other)

    def __eq__(self, other):
        return self.eval() == other

    def __deepcopy__(self, memo):
        return self

def lazify(func):
    def newfunc(*args, **kw):
        lazystr = lazystring(func, *args, **kw)
        return lazystr
    return newfunc

_lazy_gettext = lazify(_gettext)

def gettext(key, locale=None, domain=None):
    if cherrypy.request.app:
        return _gettext(key, locale, domain)
    return _lazy_gettext(key, locale, domain)

def gettext2(key, locale=None, domain=None, **kw):
    value = gettext(key, locale, domain)
    if kw:
        try:
            return value % kw or None
        except:
            pass
    return value

def install():
    __builtins__['_'] = gettext2
