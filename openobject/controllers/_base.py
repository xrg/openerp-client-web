
class ControllerType(type):
    
    def __new__(cls, name, bases, attrs):
        
        obj = super(ControllerType, cls).__new__(cls, name, bases, attrs)    
        path = attrs.get("_cp_path")
        
        if "path" in attrs and name != "BaseController":
            raise Exception("Can't override 'path' attribute.")
        
        if path:
            if not path.startswith("/"):
                raise Exception("Invalid path '%s', should start with '/'." % (path))
            
        return obj

class BaseController(object):
    
    __metaclass__ = ControllerType
    
    _cp_path = None
    
    def __new__(cls):
        return super(BaseController, cls).__new__(cls)
    
    def _get_path(self):
        return self._cp_path
    
    path = property(_get_path)

