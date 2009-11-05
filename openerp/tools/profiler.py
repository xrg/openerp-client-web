import os
import time
import logging

from os import mkdir
from os.path import dirname, join, abspath, exists

from itertools import izip, islice
from inspect import getargspec

import cherrypy
from cherrypy.lib import profiler

prof_dir = abspath(cherrypy.config.get('server.profile_dir', 'profile'))
prof_on = cherrypy.config.get('server.profile_on', False)

if prof_on and not exists(prof_dir):
    mkdir(prof_dir)

__PROFILES = {}

def to_kw(func, args, kw):

    argnames, defaults = getargspec(func)[::3]
    defaults = defaults or []
    
    kw = kw.copy()

    kv = zip(islice(argnames, 0, len(argnames) - len(defaults)), args)
    kw.update(kv)

    return args[len(argnames)-len(defaults):], kw

_RPCTIME = 0

def profile(name, log=[], cb=None):
    """
    Profile decorator.
    
    @param name: name for the profile (should be unique)og
    @param log: list of argument name to be logged, for var args give 
                index value, will be logger in sequence
    @param cb: callback to be used to log custom message then from args
    
    >>> @profile("my_say", log=[0, 2, 'something', 'format'])
    >>> def say(what, something, tosay, format=None, *args):
    >>>     ...
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(join(prof_dir, name + '.log'))
    logger.addHandler(handler)
    
    formatter = logging.Formatter("%(time)10.3f %(rpctime)10.3f %(efftime)10.3f -- %(message)s")
    handler.setFormatter(formatter)
    
    def message(fn, *args, **kw):
        
        if callable(cb):
            return "%s" % cb(*args, **kw)
        
        _a, kw = to_kw(fn, args, kw)
        
        res = []
        for n in log:
            if isinstance(n, int):
                try:
                    res.append("%s" % args[n])
                except:
                    pass
            else:
                res.append("%s=%s" % (n, kw.get(n)))
        return ", ".join(res)

    def wrapper(func):
        
        def func_wrapper(*args, **kw):
            
            global _RPCTIME
            
            rt = _RPCTIME
            
            t1 = time.time()
            res = func(*args, **kw)
            t2 = time.time()
            
            t = t2 - t1
            
            if name == "rpc.execute":
                _RPCTIME += t
                
            rt2 = _RPCTIME
            rt = rt2 - rt
            
            dct = dict(time=t, rpctime=rt, efftime=t-rt)
            logger.info(message(func, *args, **kw), extra=dct)
            
            return res
        
        func_wrapper.__name__ = func.__name__
        func_wrapper.__doc__ = func.__doc__
        func_wrapper.__dict__ = func.__dict__.copy()
        func_wrapper.__module__ = func.__module__
        return func_wrapper
        
    return wrapper

if not prof_on:
    def profile(*args, **kw):
        return lambda f: f

class ProfileViewer(object):
    
    def statfiles(self):
        if not exists(prof_dir): return []
        return [f for f in os.listdir(prof_dir) if f.endswith(".log")]
    
    def index(self):
        return """<html>
        <head><title>Profile Information</title></head>
        <frameset cols='200, 1*'>
            <frame src='menu' />
            <frame name='main' src=''/>
        </frameset>
        </html>
        """
    index.exposed = True
    
    def menu(self):
        yield "<h2>Profiling logs</h2>"
        yield "<p>Click on one of the log below to see profiling data.</p>"
        runs = self.statfiles()
        runs.sort()
        for i in runs:
            yield "<a href='report?filename=%s' target='main'>%s</a><br />" % (i, i[:-4])
        pass
    menu.exposed = True
    
    def report(self, filename):
        import cherrypy
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        yield "%10s %10s %10s\n%s\n" % ('time', 'rpctime', 'efftime', ('-' * 33))
        yield open(join(prof_dir, filename)).read()
    report.exposed = True

profile.profiler = ProfileViewer()

__builtins__['profile'] = profile

