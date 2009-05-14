from os import mkdir
from os.path import dirname, join, abspath, exists

import cherrypy
from cherrypy.lib import profiler

prof_dir = abspath(cherrypy.config.get('server.profile_dir', 'profile'))
prof_on = cherrypy.config.get('server.profile_on', False)

if prof_on and not exists(prof_dir):
    mkdir(prof_dir)

profiler = profiler.Profiler(prof_dir)

if not prof_on:
    profile = lambda func: func    
else:
    def profile(func):
        
        def wrapper(*args, **kw):
            return profiler.run(func, *args, **kw)
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__dict__ = func.__dict__.copy()
        wrapper.__module__ = func.__module__
        
        return wrapper

profile.profiler = profiler

__builtins__['profile'] = profile

