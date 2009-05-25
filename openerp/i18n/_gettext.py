import os
import sys
import string

from gettext import translation

#TODO: use Babel

import cherrypy

from openerp.i18n.utils import get_locale


__all__ = ['get_locale_dir', 'is_locale_supported', 'get_catalog', 'gettext', 'install']


_locale_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "locales"))

def get_locale_dir():
    return _locale_dir

_supported = {}
def is_locale_supported(locale, domain=None):
    try:
        return _supported[str(locale)]
    except:
        pass
    domain = domain or "messages"
    localedir = get_locale_dir()
    _supported[str(locale)] = res = localedir and os.path.exists(os.path.join(
        localedir, locale, "LC_MESSAGES", "%s.mo" % domain))
    return res

_catalogs = {}

def get_catalog(locale, domain=None):
        
    domain = domain or "messages"
    
    catalog = _catalogs.setdefault(domain, {})
    messages = catalog.get(locale)
    if not messages:
        localedir = get_locale_dir()
        messages = catalog[locale] = translation(domain=domain,
            localedir=localedir, languages=[locale])
    return messages


def _gettext(key, locale=None, domain=None):
    """Get the gettext value for key.

    Added to builtins as '_'. Returns Unicode string.

    @param key: text to be translated
    @param locale: locale code to be used.
        If locale is None, gets the value provided by get_locale.

    """
    if locale is None:
        locale = get_locale()
    if not is_locale_supported(locale):
        locale = locale[:2]
    if key == '':
        return '' # special case
    try:
        return get_catalog(locale, domain).ugettext(key)
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

