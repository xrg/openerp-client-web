import cherrypy

from openobject import pooler
from openobject.tools import expose, AuthenticationError

from _base import BaseController


class Root(BaseController):
    """Custom root controller to dispatch requests to pooled controllers.
    Based on cherrypy.dispatch.Dispatcher
    """

    @expose()
    def default(self, *args, **kw):
        try:
            obj = pooler.get_pool().get_controller("/openerp/modules")
            new_modules = obj.get_new_modules()
        except AuthenticationError:
            new_modules = []

        if new_modules:
            pooler.restart_pool()
        if 'requested_with' in kw:
            cherrypy.request.headers['X-Requested-With'] = kw.pop('requested_with')
        request = cherrypy.request
        func, vpath = self.find_handler()

        if func:
        # Decode any leftover %2F in the virtual_path atoms.
            vpath = [x.replace("%2F", "/") for x in vpath]
            request.handler = cherrypy.dispatch.LateParamPageHandler(func, *vpath)
        else:
            request.handler = cherrypy.NotFound()

        return request.handler()

    def find_handler(self):
        request = cherrypy.request
        path = request.path_info

        pool = request.pool = pooler.get_pool()

        names = [x for x in path.strip("/").split("/") if x] + ["index"]
        node = pool.get_controller("/openerp")
        trail = [["/", node]]

        curpath = ""

        for name in names:
            objname = name.replace(".", "_")
            curpath = "/".join((curpath, name))
            next = pool.get_controller(curpath)
            if next is not None:
                node = next
            else:
                node = getattr(node, objname, None)
            trail.append([curpath, node])

        # Try successive objects (reverse order)
        num_candidates = len(trail) - 1
        for i in xrange(num_candidates, -1, -1):
            curpath, candidate = trail[i]
            if candidate is None:
                continue

            # Try a "default" method on the current leaf.
            if hasattr(candidate, "default"):
                defhandler = candidate.default
                if getattr(defhandler, 'exposed', False):
                    request.is_index = path.endswith("/")
                    return defhandler, names[i:-1]

            # Try the current leaf.
            if getattr(candidate, 'exposed', False):
                if i == num_candidates:
                    # We found the extra ".index". Mark request so tools
                    # can redirect if path_info has no trailing slash.
                    request.is_index = True
                else:
                    # We're not at an 'index' handler. Mark request so tools
                    # can redirect if path_info has NO trailing slash.
                    # Note that this also includes handlers which take
                    # positional parameters (virtual paths).
                    request.is_index = False
                return candidate, names[i:-1]

        return None, []
