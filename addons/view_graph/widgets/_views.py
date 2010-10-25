from _graph import Graph
from openerp.widgets import TinyView


class GraphView(TinyView):

    _type = "graph"
    _name = _("Graph")
    _desc = _("Graph view...")
    _priority = 2

    def __call__(self, screen):

        widget = Graph(model=screen.model,
                       view=screen.view,
                       view_id=screen.view_id,
                       ids=screen.ids, domain=screen.domain,
                       view_mode = screen.view_mode,
                       context=screen.context)
        screen.ids = widget.ids
        return widget
