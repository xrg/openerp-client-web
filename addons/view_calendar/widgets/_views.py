
from openerp.widgets import TinyView

from widgets import get_calendar
from widgets import GanttCalendar

class CalendarView(TinyView):

    _type = "calendar"
    _name = _("Calendar")
    _desc = _("Calendar view...")
    _priority = 3

    def __call__(self, screen):

        widget = get_calendar(view=screen.view,
                              model=screen.model,
                              ids=screen.ids,
                              domain=screen.domain,
                              context=screen.context,
                              options=screen.kalendar)
        return widget


class GanttView(TinyView):

    _type = "gantt"
    _name = _("Gantt")
    _desc = _("Gantt view...")
    _priority = 4

    def __call__(self, screen):
        widget = GanttCalendar(model=screen.model,
                               view=screen.view,
                               ids=screen.ids,
                               domain=screen.domain,
                               context=screen.context,
                               options=screen.kalendar)
        return widget
