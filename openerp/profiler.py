import os
import time
import logging

from os import mkdir
from os.path import dirname, join, abspath, exists

import cherrypy
from cherrypy.lib import profiler

prof_dir = abspath(cherrypy.config.get('server.profile_dir', 'profile'))
prof_on = cherrypy.config.get('server.profile_on', False)

if prof_on and not exists(prof_dir):
    mkdir(prof_dir)

__PROFILES = {}


def profile(name, arange=[], keys=[]):
    """
    Profile decorator.
    
    @param name: name for the profile (should be unique)
    @param arange: list argument indices to be used to log
    @params keys: list of keys to be used to log
    
    >>> @profile("my_say", arange=[0,2], keys=['format'])
    >>> def say(what, something, tosay, format=None):
    >>>     ...
    """
    
    assert name not in __PROFILES, "duplicate profile name %s, should be unique." % name
    
    tinfo = __PROFILES.setdefault(name, {'ncalls': 0, 'tottime': 0.0})
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(join(prof_dir, name + '.log'))
    logger.addHandler(handler)
    
    formatter = logging.Formatter("%(percall)10.3f %(rpctime)10.3f %(efftime)10.3f -- %(message)s")
    handler.setFormatter(formatter)
    
    def message(args, kw):
        
        res = []
        for i in arange:
            try:
                res.append("%s" % (args[i]))
            except:
                pass
        for k in keys:
            res.append("%s=%s" % (k, kw.get(k)))
        return ", ".join(res)

    def wrapper(func):
        
        def func_wrapper(*args, **kw):
            
            rt = __PROFILES.get('rpc.execute', {}).get('tottime', 0.0)
            
            nc = tinfo['ncalls'] = tinfo['ncalls'] + 1
            
            t1 = time.time()
            res = func(*args, **kw)
            t2 = time.time()
            
            t = t2 - t1
            tt = tinfo['tottime'] = tinfo['tottime'] + t
            
            rt2 = __PROFILES.get('rpc.execute', {}).get('tottime', 0.0)
            rt = rt2 - rt
            
            dct = dict(percall=tt/nc, rpctime=rt, efftime=t-rt, tottime=tt)
            logger.info(message(args, kw), extra=dct)
            
            return res
        
        func_wrapper.__name__ = func.__name__
        func_wrapper.__doc__ = func.__doc__
        func_wrapper.__dict__ = func.__dict__.copy()
        func_wrapper.__module__ = func.__module__
        return func_wrapper
        
    return wrapper

if not prof_on:
    def profile(name):
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
            yield "<a href='report?filename=%s' target='main'>%s</a><br />" % (i, i)
        pass
    menu.exposed = True
    
    def report(self, filename):
        import cherrypy
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        yield "%10s %10s %10s\n%s\n" % ('percall', 'rpctime', 'efftime', ('-' * 33))
        yield open(join(prof_dir, filename)).read()
    report.exposed = True

profile.profiler = ProfileViewer()

__builtins__['profile'] = profile

