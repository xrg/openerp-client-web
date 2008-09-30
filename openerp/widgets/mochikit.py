from turbogears.widgets import Widget
from turbogears.widgets import JSLink

class MochiKit(Widget):
    javascript = [JSLink("openerp", "javascript/MochiKit/MochiKit.js"),
                  JSLink("openerp", "javascript/MochiKit/DragAndDrop.js"),
                  JSLink("openerp", "javascript/MochiKit/Resizable.js"),
                  JSLink("openerp", "javascript/MochiKit/Sortable.js")]

mochikit = MochiKit()

