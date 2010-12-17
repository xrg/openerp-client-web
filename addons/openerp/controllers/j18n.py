# -*- coding: utf-8 -*-
import babel
import cherrypy

import openobject.controllers
import openobject.i18n
import openobject.tools

class J18N(openobject.controllers.BaseController):
    _cp_path = '/openerp/j18n'

    @openobject.tools.expose('jsonp')
    def default(self, locale_string):
        # We're abusing a bit the expose(jsonp) implementation here by
        # forcing the callback JSONP handlers generally receive via their
        # params (and @expose gets from there)
        cherrypy.request.params['callback'] = 'openobject.gettext.update'
        try:
            # babel.support.Translations._catalog, inherited from
            # gettext.GNUTranslation, is the trivial mapping of msgid to
            # translated text as a Python dict. Therefore we can return
            # just that and it'll get dumped just right for the jsonp
            # callback.
            catalog = openobject.i18n.get_translations(
                    babel.core.Locale.parse(locale_string),
                    domain='javascript'
                    )._catalog
            # remove the empty key as it maps to the PO header
            if '' in catalog: del catalog['']
            return catalog
        except KeyError:
            return {}
