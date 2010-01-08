
import cherrypy
import addons
import pooler

class Dispatcher(cherrypy.dispatch.Dispatcher):
    
    def find_handler(self, path):
        
        request = cherrypy.request
        app = request.app
        root = app.root

        pool = pooler.get_pool(app.config)
        
        if path == "/":
            root = pool.get_controller("") or app.root
        
        # Get config for the root object/path.
        curpath = ""
        nodeconf = {}
        if hasattr(root, "_cp_config"):
            nodeconf.update(root._cp_config)
        if "/" in app.config:
            nodeconf.update(app.config["/"])
        object_trail = [['root', root, nodeconf, curpath]]
        
        node = root
        names = [x for x in path.strip('/').split('/') if x] + ['index']
        for name in names:
            # map to legal Python identifiers (replace '.' with '_')
            objname = name.replace('.', '_')
            
            nodeconf = {}
            
            if node is None:
                node = pool.get_controller(curpath)
            else:
                node = getattr(node, objname, None)
                
            if node is not None:
                # Get _cp_config attached to this node.
                if hasattr(node, "_cp_config"):
                    nodeconf.update(node._cp_config)
            
            # Mix in values from app.config for this path.
            curpath = "/".join((curpath, name))
            if curpath in app.config:
                nodeconf.update(app.config[curpath])
            
            object_trail.append([name, node, nodeconf, curpath])
        
        def set_conf():
            """Collapse all object_trail config into cherrypy.request.config."""
            base = cherrypy.config.copy()
            # Note that we merge the config from each node
            # even if that node was None.
            for name, obj, conf, curpath in object_trail:
                base.update(conf)
                if 'tools.staticdir.dir' in conf:
                    base['tools.staticdir.section'] = curpath
            return base
        
        # Try successive objects (reverse order)
        num_candidates = len(object_trail) - 1
        for i in xrange(num_candidates, -1, -1):
            
            name, candidate, nodeconf, curpath = object_trail[i]
            if candidate is None:
                continue
            
            # Try a "default" method on the current leaf.
            if hasattr(candidate, "default"):
                defhandler = candidate.default
                if getattr(defhandler, 'exposed', False):
                    # Insert any extra _cp_config from the default handler.
                    conf = getattr(defhandler, "_cp_config", {})
                    object_trail.insert(i+1, ["default", defhandler, conf, curpath])
                    request.config = set_conf()
                    # See http://www.cherrypy.org/ticket/613
                    request.is_index = path.endswith("/")
                    return defhandler, names[i:-1]
            
            # Uncomment the next line to restrict positional params to "default".
            # if i < num_candidates - 2: continue
            
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
                print "RRRRRRRRR", candidate, names[i:-1]
                return candidate, names[i:-1]
        
        # We didn't find anything
        request.config = set_conf()
        return None, []

