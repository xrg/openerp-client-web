import cherrypy

class CPSessionWrapper(object):

    def __setattr__(self, name, value):
        cherrypy.session[name] = value

    def __getattr__(self, name):
        return cherrypy.session.get(name)

    def __delattr__(self, name):
        if name in cherrypy.session:
            del cherrypy.session[name]

    __getitem__ = __getattr__
    __setitem__ = __setattr__

    def get(self, name, default=None):
        return cherrypy.session.get(name, default)

    def clear(self):
        cherrypy.session.clear()

def init_rpc_session():

    config = cherrypy.config

    # initialize the rpc session
    host = config.get('openerp.server.host')
    port = config.get('openerp.server.port')
    protocol = config.get('openerp.server.protocol')

    import rpc
    rpc.initialize(host, port, protocol, storage=CPSessionWrapper())

init_rpc_session()
