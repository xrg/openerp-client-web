import cherrypy

_REGISTRY = {}

def register_object(obj, key, group, auto_create=False):
    """Register and object with key in the given group.

    @param obj: the object to register
    @param key: key to access the register object from the pool
    @param group: the group in which the object should be registered
    @auto_create: if True create and instance of the object during pool.initialize

    >>>
    >>> pooler.register_object(klass, "char", group="form_input_widgets")
    >>> pooler.register_object(klass, "/about", group="controllers")
    >>> pooler.register_object(klass, "calendar", group="view_type")
    >>>
    """

    module = None
    if hasattr(obj, '__module__'):
        module = str(obj.__module__).split('.')[0]

    registry = _REGISTRY.setdefault(group, {})
    objects = registry.setdefault(module, {})
    assert isinstance(obj, type), 'You can only register classes to the pooler'

    objects[key] = (auto_create, obj)

class Pool(object):

    def __init__(self):
        self.obj_pool = {}
        self.ready = False

    def get(self, key, group):
        return self.get_group(group).get(key, None)

    def get_group(self, key):
        assert self.ready, "This object pool isn't ready for usage yet, please finalize() it"
        return self.obj_pool.get(key, {})

    def get_controller(self, name):
        return self.get(name, "controllers")

    def load(self, package):
        ''' Loads all the objects of the provided package in the current pooler
        '''
        for group, registry in _REGISTRY.items():
            if package in registry:
                for key, (auto_create, obj) in registry[package].items():
                    objects = self.obj_pool.setdefault(group, {})
                    objects.setdefault(key, []).append((auto_create, obj))

    def finalize(self):
        ''' Folds objects by handling inheritance between different modules
        '''
        assert not self.ready, "Don't finalize an already ready pool"
        for objects in self.obj_pool.itervalues():
            for key, typ in objects.iteritems():
                if len(typ) > 1:
                    auto_creates, types = zip(*typ)
                    auto_create = any(auto_creates)
                    obj_type = type(
                            types[-1].__name__, # use name of last type in sequence
                            tuple(reversed(types)), # MRO will use first base first, and we want last add-on first
                            {}) # no additional variables?
                else:
                    auto_create, obj_type = typ[0]
                if auto_create:
                    objects[key] = obj_type()
                else:
                    objects[key] = obj_type
        self.ready = True
        return self

pool_dict = {}

def restart_pool():
    
    db_name = cherrypy.session['db']
    
    if db_name in pool_dict:
        import addons
        
        del pool_dict[db_name]
        del addons._loaded[db_name]
    
    return get_pool()
        
def get_pool():

    config = cherrypy.request.app.config
    db_name = None

    try:
        db_name = cherrypy.session['db']
    except Exception, e:
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
        pool.finalize()

    return pool
