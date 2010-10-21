import cherrypy

_REGISTRY = {}

def register_object(cls, key, group):
    """Register and object with key in the given group.

    @param cls: the type to register
    @param key: key to access the registered type from the pool
    @param group: the group in which the type should be registered

    >>>
    >>> pooler.register_object(cls, "char", group="form_input_widgets")
    >>> pooler.register_object(cls, "/about", group="controllers")
    >>> pooler.register_object(cls, "calendar", group="view_type")
    >>>
    """
    assert isinstance(cls, type), 'You can only register classes to the pooler'
    module = None
    if hasattr(cls, '__module__'):
        module = str(cls.__module__).split('.')[0]

    registry = _REGISTRY.setdefault(group, {})
    group_types = registry.setdefault(module, {})

    group_types[key] = cls

class Pool(object):

    def __init__(self):
        self.types_pool = {}

    def get(self, key, group):
        return self.get_group(group).get(key, None)

    def get_group(self, key):
        return self.types_pool.get(key, {})

    def get_controller(self, name):
        """ Fetches and initializes a controller instance
        """
        Controller = self.get(name, "controllers")
        if Controller: return Controller()
        return None

    def load(self, package):
        ''' Loads all the objects of the provided package in the current pooler
        '''
        for group, registry in _REGISTRY.iteritems():
            if package in registry:
                for key, typ in registry[package].iteritems():
                    types = self.types_pool.setdefault(group, {})
                    if key in types and typ not in types[key].mro():
                        # already have an object there, build subtype
                        types[key] = type(typ.__name__,
                                          (typ, types[key]),
                                          {})
                    else:
                        types[key] = typ

pool_dict = {}

def restart_pool():

    print dict(cherrypy.session)
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

    return pool
