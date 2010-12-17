import os

from openobject import i18n

from _resource import JSLink


class JSI18n(JSLink):
    template = "/openobject/widgets/templates/js_i18n.mako"

    params = ["locale"]
    def update_params(self, params):
        super(JSLink, self).update_params(params)
        params['locale'] = i18n.get_locale()


js_i18n = JSI18n(None, None)
