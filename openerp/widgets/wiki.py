
from form import Text
import turbogears as tg
from StringIO import StringIO

class Wiki(Text):
    template = "openerp.widgets.templates.wiki"
    
    params = ["url", "title", "data", "id", "string", "tg_css", "inline"]
    css = [tg.widgets.CSSLink('openerp', 'css/wiki.css')]
    javascript = [tg.widgets.JSLink("openerp", "javascript/textarea.js")]
    
    def __init__(self, attrs):
        super(Wiki, self).__init__(attrs)
        self.data = ""

    def set_value(self, value):
        super(Wiki, self).set_value(value)
        
        if value:
            from tinywiki import parse
            text = value+'\n\n'
            html = parse(text, True)
            self.data = html
            
#            input = StringIO(value+'\n\n')
#            parser = Wiki2Html.Wiki2Html()
#            parser.read(input)
#            html = parser.html
#            self.data = html