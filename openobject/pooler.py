
import cherrypy


_REGISTRY = {}

def register_class(klass, kind):
    
    module = str(klass.__module__).split('.')[0]
    registry = _REGISTRY.setdefault(kind, {})
    objects = registry.setdefault(module, [])
    
    if klass not in objects:
        objects.append(klass)
        
    return klass


class Pool(object):
    
    def __init__(self):
        self.obj_pool = {"controller": {}, "widget": {}, "validator": {}}
        
    def get_controller(self, name):        
        return self.obj_pool["controller"].get(name, None)
    
    def get_validator(self, name):
        return self.obj_pool["validator"].get(name, None)
    
    def get_widget(self, name):
        return self.obj_pool["widget"].get(name, None)
    
    def instanciate(self, package):
        
        for key in ("controller", "widget", "validator"):
            objects = _REGISTRY.get(key, {}).get(package, [])
            for obj in objects:
                if key == "controller":
                    name = getattr(obj, '_cp_path')
                    if name:
                        self.obj_pool[key][name] = obj()
                if key == "widget":
                    name = getattr(obj, '_data_type')
                    if name:
                        self.obj_pool[key][name] = obj
                if key == "validator":
                    name = getattr(obj, '_data_type')
                    if name:
                        self.obj_pool[key][name] = obj


pool_dict = {}

def get_pool(config):
    
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

