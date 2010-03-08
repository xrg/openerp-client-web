import os

from itertools import imap
from itertools import izip
from itertools import chain

import cherrypy

from _base import Widget
from _utils import OrderedSet
from _utils import Enum

from openobject import tools

locations = Enum(["head", "bodytop", "bodybottom"])


# a random id to be used to generate static js/css links to prevent cache
import random
try:
    from hashlib import sha1 as sha
except:
    from sha import new as sha

_UUID = sha('%s' % random.random()).hexdigest()


class Resource(Widget):

    location = locations.head

    @property
    def name(self):
        return None


class Link(Resource):

    params = {
        'link': None,
    }

    _filename = None
    modname = None

    def __init__(self, modname, filename, location=locations.head, **kw):
        super(Link, self).__init__(modname=modname, location=location, **kw)
        self._filename = filename

    def get_link(self):

        link = "/%s/static/%s" % (self.modname, self.filename)
        if cherrypy.config.get('server.environment') == 'development':
            link = "%s?%s" % (link, _UUID)
        return tools.url(link)

    def get_file(self):
        return self._filename

    link = property(lambda self: self.get_link())
    filename = property(lambda self: self.get_file())

    def __eq__(self, other):
        return getattr(other, 'link', None) == self.link

    def __hash__(self):
        return hash(self.link)


class JSLink(Link):

    template = """\
    <script type="text/javascript" src="${link}" ${py.attrs(charset=charset, defer=defer)}></script>\
    """

    params = {
        'charset': 'The character encoding of the linked script',
        'defer': 'If true, browser may defer execution of the script'
    }

    charset = None
    defer = None


class CSSLink(Link):

    params = {
        'media': 'Specify the media attribute for the css link tag'
    }

    template = """\
    <link rel="stylesheet" type="text/css" href="${link}" ${py.attrs(media=media)}/>\
    """


class Source(Resource):

    params = {
        'src': 'The source text',
    }

    def __init__(self, src, location=locations.head, **kw):
        super(Source, self).__init__(src=src, location=location, **kw)

    def __hash__(self):
        return hash(self.src)

    def __eq__(self, other):
        return self.src == getattr(other, 'src', None)


class JSSource(Source):
    """A JavaScript source snippet."""

    template = """\
    <script type="text/javascript" ${py.attrs(defer=defer)}>
        ${src|n}
    </script>\
    """

    params = {
        'defer': 'If true, browser may defer execution of the script'
    }


class CSSSource(Source):
    """A CSS source snippet."""

    template = """\
    <style type="text/css" ${py.attrs(media=media)}>
        ${src|n}
    </style>\
    """

    params = {
        'src': 'The CSS source for the link',
        'media' : 'Specify the media the css source link is for'
    }

    media = "all"

def register_resource_directory(config, modulename, directory):
    """Set up an application wide static resource directory...
    """

    #assert isinstance(app, cherrypy.Application), "Excepected cherrypy.Application"

    directory = os.path.abspath(directory)
    config.update({'/%s/static' % modulename: {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': directory
    }})
