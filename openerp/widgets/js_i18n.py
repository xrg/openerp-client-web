from turbogears import startup
from turbogears.i18n import tg_gettext

from turbogears.widgets import Widget
from turbogears.widgets import JSLink

def _get_locale():
    lang = tg_gettext.get_locale()
    if len(lang) == 2:
        lang = lang + '_' + lang
    if len(lang) > 2:
        country = lang[3:].upper()
        lang = lang[:2] + "_" + country
    return lang

class JSCatelog(JSLink):
    def update_params(self, d):
        super(JSCatelog, self).update_params(d)
        lang = _get_locale()
        if tg_gettext.is_locale_supported(lang):
            d["link"] = "/%sstatic/javascript/i18n/%s.js" % (startup.webpath, lang)

class JSI18n(Widget):
    javascript = [JSLink('openerp', 'javascript/i18n/i18n.js'),
                  JSCatelog('openerp', 'javascript/i18n/en_EN.js'),]

js_i18n = JSI18n()


# Auto generate language files from gettext catalogs.

import os
import pkg_resources
from turbojson import jsonify

def __generate_catalog(locale):

    if not tg_gettext.is_locale_supported(locale):
        return

    fname = pkg_resources.resource_filename("openerp",  "static/javascript/i18n/%s.js" % locale)
    cname = os.path.join(tg_gettext.get_locale_dir(), locale, 'LC_MESSAGES', 'messages.mo')

    if os.path.exists(fname) and os.path.getmtime(fname) >= os.path.getmtime(cname):
        return

    print "Generating JavaScript i18n message catalog for %s..." % locale
    messages = {}
    try:
        messages = tg_gettext.get_catalog(locale=locale)._catalog
        messages.pop("")
    except Exception, e:
        pass
    messages = jsonify.encode(messages)

    catalog = """
// Auto generated file. Please don't modify.
var MESSAGES = %(messages)s;

""" % dict(messages=messages)

    try:
        fo = open(fname, 'w')
        fo.write(catalog)
        fo.close()
    except Exception, e:
        pass

def __generate_catalogs():
    for lang in os.listdir(tg_gettext.get_locale_dir()):
        __generate_catalog(lang)

__generate_catalogs()

# vim: ts=4 sts=4 sw=4 si et

