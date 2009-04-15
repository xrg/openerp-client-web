import os

from itertools import izip, chain, imap

import cherrypy

from openerp.widgets.base import Widget
from openerp.widgets.utils import OrderedSet
from openerp.widgets.utils import Enum


locations = Enum(["head", "bodytop", "bodybottom"])


class Resource(Widget):

    location = locations.head

    def post_init(self, *args, **kw):
        self._resources.add(self)

    @property
    def name(self):
        return None


class Link(Resource):

    params = {
        'link': None,
    }

    filename = None
    modname = None

    def __init__(self, modname, filename, location=locations.head, **kw):
        super(Link, self).__init__(modname=modname, filename=filename, location=location, **kw)

        #TODO: consider the server.webpath and cherrypy mount point
        self.link = "/cp_widgets/%s/%s" % (self.modname, self.filename)

    def __eq__(self, other):
        return getattr(other, 'link', None) == self.link

    def __hash__(self):
        return hash(self.link)


class JSLink(Link):

    template = """\
    <script type="text/javascript" src="${link}" charset="${charset}" defer="${defer and 'defer' or ''}"></script>\
    """

    params = {
        'charset': 'The character encoding of the linked script',
        'defer': 'If true, browser may defer execution of the script'
    }

    charset = None
    defer = False


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
    <script type="text/javascript" defer="${defer and 'defer' or None}">
        ${src}
    </script>\
    """

    params_doc = {
        'defer': 'If true, browser may defer execution of the script'
    }

    defer = False


class CSSSource(Source):
    """A CSS source snippet."""

    template = """\
    <style type="text/css" media="${media}">
        ${src}
    </style>\
    """

    params = {
        'src': 'The CSS source for the link',
        'media' : 'Specify the media the css source link is for'
    }

    media = "all"


def merge_resources(to, from_):
    """
    In-place merge all resources from ``from_`` into ``to``. Resources
    from ``to_`` will come first in each resulting OrderedSet.
    """
    for k in locations:
        from_location = from_.get(k)
        if from_location:
            to.setdefault(k, OrderedSet()).add_all(from_location)
    return to


def retrieve_resources(obj):
    """Recursively retrieve resources from obj"""
    ret = {}
    if getattr(obj, 'retrieve_resources', None):
        ret = obj.retrieve_resources()
    elif getattr(obj, 'itervalues', None):
        ret = retrieve_resources(obj.itervalues())
    elif getattr(obj, '__iter__', None):
        ret = reduce(merge_resources, imap(retrieve_resources, iter(obj)), {})
    return ret

def register_resource_directory(app, modulename, directory):
    """Set up an application wide static resource directory...
    """

    assert isinstance(app, cherrypy.Application), "Excepected cherrypy.Application"

    directory = os.path.abspath(directory)
    app.config.update({'/cp_widgets/%s' % modulename: {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': directory
    }})

