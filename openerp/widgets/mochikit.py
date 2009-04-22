from openerp.widgets.base import Widget
from openerp.widgets.base import JSLink

class MochiKit(Widget):
    javascript = [JSLink("openerp", "javascript/MochiKit/MochiKit.js"),
                  JSLink("openerp", "javascript/MochiKit/DragAndDrop.js"),
                  JSLink("openerp", "javascript/MochiKit/Resizable.js"),
                  JSLink("openerp", "javascript/MochiKit/Sortable.js")]

mochikit = MochiKit()

