from turbogears import startup

from turbogears.widgets import Widget
from turbogears.widgets import JSLink

class JSCatelog(JSLink):
    def update_params(self, d):
        super(JSCatelog, self).update_params(d)
        d["link"] = "/%s%s" % (startup.webpath, self.name)

class JSI18n(Widget):
    javascript = [JSCatelog("/", "messages.js"),]

js_i18n = JSI18n()

