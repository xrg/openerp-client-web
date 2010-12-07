import os

from openobject import i18n

from _resource import JSLink


class JSI18n(JSLink):
    template = "/openobject/widgets/templates/js_i18n.mako"

    params = ["translations"]
    def update_params(self, params):
        super(JSLink, self).update_params(params)

        locale = i18n.get_locale()
        try:
            trans = i18n.get_translations(locale, domain="javascript")
        except KeyError:
            trans = []

        translations = []

        static_dir = "%sstatic%s" % (os.path.sep, os.path.sep)
        for tr in trans:
            pr, tr = tr.split(static_dir)
            _, pr = os.path.split(pr)
            translations.append((pr, tr))

        params['translations'] = translations


js_i18n = JSI18n(None, None)
