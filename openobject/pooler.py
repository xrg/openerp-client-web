
import cherrypy


_REGISTRY = {}

def register_object(obj, key, group, auto_create=False):
    
    module = None
    if hasattr(obj, '__module__'):
        module = str(obj.__module__).split('.')[0]
        
    registry = _REGISTRY.setdefault(group, {})
    objects = registry.setdefault(module, {})
    
    if auto_create:
        objects[key] = lambda: obj()
    else:
        objects[key] = lambda: obj
    
class Pool(object):
    
    def __init__(self):
        self.obj_pool = {}
        
    def get(self, key, group):
        return self.obj_pool.get(group, {}).get(key, None)
    
    def get_group(self, key):
        return self.obj_pool.get(group, {})
    
    def get_controller(self, name):
        return self.get(name, "controllers")
    
    def instanciate(self, package):
        for group, groups in _REGISTRY.items():
            for module, modules in groups.items():
                for name, obj in modules.items():
                    objects = self.obj_pool.setdefault(group, {})
                    objects[name] = obj()

pool_dict = {}

def get_pool():
    
    config = cherrypy.request.app.config    
    db_name = None
    
    try:
        db_name = cherrypy.session.db
    except:
        pass
    
    if db_name in pool_dict:
        pool = pool_dict[db_name]
    else:
        import addons
        
        pool = pool_dict[db_name] = Pool()
        
        try:
            addons.load_addons(db_name, config)
        except:
            del pool_dict[db_name]
            raise
        
    return pool

