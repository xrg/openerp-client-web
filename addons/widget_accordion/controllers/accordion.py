from openobject.tools import expose
from openobject.controllers import BaseController

class AccordionDemo(BaseController):
    
    _cp_path = "/accordion"
    
    @expose(template="templates/accordion.mako")
    def index(self):
        return dict()
