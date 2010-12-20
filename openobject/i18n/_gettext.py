from __future__ import with_statement

import hashlib
import glob
import tempfile
import os
from os.path import basename, exists, getmtime, isdir, join, splitext

import cherrypy

import babel
import babel.messages.mofile
import babel.messages.pofile
import babel.support

from openobject.i18n.utils import get_locale


__all__ = ['get_translations', 'load_translations', 'gettext', 'install']


_translations = {}
_machine_objects_cache = tempfile.mkdtemp()

def get_translations(locale, domain=None):
    domain = domain or "messages"

    domain_catalog = _translations.setdefault(domain, {})

    if locale in domain_catalog:
        return domain_catalog[locale]
    return domain_catalog[locale.language]

def _load_translation(path, locale, domain):
    """ Loads the locale's translation for the addon at the provided path
    :param path: an addon's path, should contain a po/messages subdir
    :type path: str
    :param locale: the locale to load
    :type locale: babel.Locale
    :param domain: the domain to load the translation in (and from)
    :type domain: str
    :rtype: babel.support.Translations | gettext.NullTranslation
    """
    locale_path = join(_machine_objects_cache,
                       hashlib.md5(path).hexdigest()[:8], 'locale')
    popath = join(path, 'po', domain, '%s.po' % locale)
    modir = join(locale_path, str(locale), 'LC_MESSAGES')
    if not exists(modir):
        os.makedirs(modir, 0700)
    mopath = join(modir, domain + '.mo')

    if not exists(mopath) or getmtime(mopath) < getmtime(popath):
        # generate MO file if none exists or the MO file is older than the PO
        # file (== the PO file got updated since the cache was built)
        with open(popath, 'rb') as pofile:
            with open(mopath, 'wb') as mofile:
                babel.messages.mofile.write_mo(
                        mofile,
                        babel.messages.pofile.read_po(
                                pofile, locale, domain))
    return babel.support.Translations.load(
            locale_path, [locale], domain)

def _load_translations(path, locales, domain):
    if not locales:
        locales = (
            splitext(basename(p))[0]
            for p in glob.glob(join(path, 'po', domain, '*.po')))

    catalog = _translations.setdefault(domain, {})
    for locale in locales:
        try:
            tr = _load_translation(path, locale, domain)
        except SyntaxError, e:
            # http://babel.edgewall.org/ticket/213
            cherrypy.log.error('Syntax error during translations loading', traceback=True)
            tr = None
        if isinstance(tr, babel.support.Translations):
            if locale in catalog:
                catalog[locale].merge(tr)
            else:
                catalog[locale] = tr

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
    :type domain: str
    """
    _load_translations(path, locales, domain)

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
