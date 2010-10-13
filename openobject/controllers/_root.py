import cherrypy

from openobject import pooler
from openobject.tools import expose, AuthenticationError

from _base import BaseController
import pprint


class Root(BaseController):
    """Custom root controller to dispatch requests to pooled controllers.
    Based on cherrypy.dispatch.Dispatcher
    """

    # header: query param mapping
    custom_headers = [
        # Header set by XHR requests, used to know whether the client needs
        # a full template (including JS and CSS files) or just the content
        # area of the HTML
        ('X-Requested-With', 'requested_with')
    ]
    def reset_custom_headers_post_redirection(self, request):
        """ Firefox doesn't forward headers it has no reason to touch
        (standard or custom headers, does't matter) during redirection.

        To try and fix that, we're setting the headers we need forwarded as
        query parameters during the redirection process, but we're still
        reading them as headers (so as not to special case the code using
        them, and all the stuff that can be called after a redirection).

        This method transfers those custom headers that had been stored as
        query params back into request headers, as far as the userland
        code is concerned anyway.

        Firefox bug ref: https://bugzilla.mozilla.org/show_bug.cgi?id=553888
        """
        for header, param in self.custom_headers:
            if param not in request.params: continue
            value = request.params.pop(param)
            # only set if not already there, you never know, we could have
            # a bug in our own code as well
            if header not in request.headers:
                request.headers[header] = value

    @expose()
    def default(self, *args, **kw):
        try:
            obj = pooler.get_pool().get_controller("/openerp/modules")
            new_modules = obj.get_new_modules()
        except AuthenticationError:
            new_modules = []

        if new_modules:
            pooler.restart_pool()

        request = cherrypy.request
        self.reset_custom_headers_post_redirection(request)
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
