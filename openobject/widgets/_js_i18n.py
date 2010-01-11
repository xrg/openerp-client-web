import os

from openobject import i18n
from openobject import tools

from _base import Widget
from _resource import JSLink


class JSI18n(JSLink):
    
    template = """\
    % for m, tr in translations:
        <script type="text/javascript" src="/${m}/static/javascript/${tr}"></script>
    % endfor
    """
    
    params = ["translations"]
    def update_params(self, d):
        
        super(JSLink, self).update_params(d)
        
        locale = i18n.get_locale()
        trans = i18n.get_translations(locale, domain="javascript") or []
        
        translations = []
        
        for tr in trans:
            pr, tr = tr.split("/static/")
            pr = pr.split("/")[-1]
            translations.append((pr, tr))
            
        d.translations = translations
        

js_i18n = JSI18n(None, None)


# vim: ts=4 sts=4 sw=4 si et

