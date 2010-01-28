import cherrypy

from openobject import pooler
from openobject.tools import expose

from _base import BaseController


class Root(BaseController):
    """Custom root controller to dispatch requests to pooled controllers.
    Based on cherrypy.dispatch.Dispatcher
    """
    
    @expose()
    def __call__(self, *args, **kw):
        request = cherrypy.request
        func, vpath = self.find_handler()
                
        if func:
            # Decode any leftover %2F in the virtual_path atoms.
            vpath = [x.replace("%2F", "/") for x in vpath]
            request.handler = cherrypy.dispatch.LateParamPageHandler(func, *vpath)
        else:
            request.handler = cherrypy.NotFound()
                    
    def find_handler(self):
        
        request = cherrypy.request
        path = request.path_info
        app = request.app
        
        pool = request.pool = pooler.get_pool()
        
        names = [x for x in path.strip("/").split("/") if x] + ["index"]
                
        node = pool.get_controller("/")
     
        curpath = ""
        nodeconf = {}
        
        if hasattr(node, "_cp_config"):
            nodeconf.update(node._cp_config)
            
        if "/" in app.config:
            nodeconf.update(app.config["/"])
        trail = [['/', node, nodeconf, curpath]]
          
        for name in names:
            objname = name.replace(".", "_")
            curpath = "/".join((curpath, name))
            nodeconf = {}
            next = pool.get_controller(curpath)
            if next is not None:
                node = next
            else:
                node = getattr(node, objname, None)
                
            if node is not None:
                if hasattr(node, "_cp_config"):
                    nodeconf.update(node._cp_config)
                    
            if curpath in app.config:
                nodeconf.update(app.config[curpath])
                
            trail.append([name, node, nodeconf, curpath])
    
        def set_conf():
            base = cherrypy.config.copy()
            for name, obj, conf, curpath in trail:
                 base.update(conf)
                 if 'tools.staticdir.dir' in conf:
                     base['tools.staticdir.section'] = curpath
            return base
            
        # Try successive objects (reverse order)
        num_candidates = len(trail) - 1
        for i in xrange(num_candidates, -1, -1):
            
            name, candidate, nodeconf, curpath  = trail[i]
            if candidate is None:
                continue
                        
            # Try a "default" method on the current leaf.
            if hasattr(candidate, "default"):
                defhandler = candidate.default
                if getattr(defhandler, 'exposed', False):
                    conf = getattr(defhandler, "_cp_config", {})
                    trail.insert(i+1, ["default", defhandler, conf, curpath])
                    request.config = set_conf()
                    request.is_index = path.endswith("/")
                    return defhandler, names[i:-1]
                    
            # Try the current leaf.
            if getattr(candidate, 'exposed', False):
                request.config = set_conf()
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
        request.config = set_conf()
        return None, []
    
