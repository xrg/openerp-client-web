import glob
import os
from os.path import basename, exists, isdir, join, splitext

import cherrypy

import babel
import babel.support

from openobject.i18n.utils import get_locale


__all__ = ['get_translations', 'load_translations', 'gettext', 'install']


_translations = {}


def get_translations(locale, domain=None):
    domain = domain or "messages"

    domain_catalog = _translations.setdefault(domain, {})

    if locale in domain_catalog:
        return domain_catalog[locale]
    return domain_catalog[locale.language]

def _load_messages_translations(locales, path):
    locale_path = join(path, 'locale')
    if not isdir(locale_path): return

    if not locales:
        locales = (
            splitext(basename(p))[0]
            for p in glob.glob(join(path, 'po', 'messages', '*.po')))

    catalog = _translations.setdefault('messages', {})
    for locale in locales:
        tr = babel.support.Translations.load(
                locale_path, [locale], 'messages')
        if isinstance(tr, babel.support.Translations):
            if locale in catalog:
                catalog[locale].merge(tr)
            else:
                catalog[locale] = tr

def _load_javascript_translations(locales, path):
    catalog = _translations.setdefault('javascript', {})
    jspath = join(path, "static", "javascript", "i18n")
    if not isdir(jspath): return
    if not locales:
        locales = [splitext(f)[0]
                   for f in os.listdir(jspath)]
    for locale in locales:
        fname = join(jspath, "%s.js" % locale)
        if exists(fname):
            _all = catalog.setdefault(locale, [])
            _all.append(fname)

_translations_loaders = {
    'messages': _load_messages_translations,
    'javascript': _load_javascript_translations
}
def load_translations(path, locales=None, domain="messages"):
    """
    :param path: the root of the addon from which the translation will be
                 loaded (should probably have at least a filled 'po'
                 directory)
    :type path: str
    :param locales: a list of locales to load, loads all locales if
                    none provide
    :type locales: [str] or None
    :param domain: the domain to load
    :type domain: "messages" | "javascript"
    """
    _translations_loaders[domain](locales, path)

def _gettext(key, locale=None, domain=None):
    """Get the gettext value for key.

    Added to builtins as '_'. Returns Unicode string.

    @param key: text to be translated
    @param locale: locale code to be used.
        If locale is None, gets the value provided by get_locale.

    """
    if locale is None:
        locale = get_locale()
    elif not isinstance(locale, babel.Locale):
        locale = babel.Locale.parse(locale)
    if key == '':
        return '' # special case
    try:
        return get_translations(locale, domain).ugettext(key)
    except KeyError:
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
