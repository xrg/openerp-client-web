from openerp.widgets import TinyView

from diagram import Diagram


class DiagramView(TinyView):
    _type = "diagram"
    _name = _("Diagram")
    _desc = _("Diagram view...")
    _priority = 5

    def __call__(self, screen):
        widget = Diagram(name=screen.name,
                         model=screen.model,
                         view=screen.view,
                         ids=((screen.id or []) and [screen.id]) or screen.ids[:1],
                         domain=screen.domain,
                         context=screen.context)
        if not screen.id:
            screen.id = screen.ids[0]

        return widget
