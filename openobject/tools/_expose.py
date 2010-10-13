###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

import re

import cherrypy
import simplejson

from mako.template import Template
from mako.lookup import TemplateLookup

from openobject import templating

import _utils as utils
import resources


__all__ = ['load_template', 'render_template', 'expose', 'register_template_vars']


# ask autoreloader to check mako templates and cfg files
for res in resources.find_resources("openobject", "..", ["*.mako", "*.cfg"]):
    cherrypy.engine.autoreload.files.add(res)


filters = ["__content"]
imports = ["from openobject.tools import content as __content"]

class TL(TemplateLookup):

    cache = {}

    def get_template(self, uri):
        try:
            return self.cache[str(uri)]
        except Exception, e:
            pass
        self.cache[str(uri)] = res = super(TL, self).get_template(uri)
        return res

template_lookup = TL(directories=[resources.find_resource("openobject", ".."),
                                  resources.find_resource("openobject", "../addons")],
                     default_filters=filters,
                     imports=imports,
                     preprocessor=templating.edition_preprocessor)

def load_template(template):

    if not isinstance(template, basestring):
        return template

    if re.match('(.+)\.(html|mako)\s*$', template):
        return template_lookup.get_template(template)
    else:
        return Template(template, default_filters=filters, imports=imports)


class _Provider(dict):

    def __getattr__(self, name):
        if name in self:
            return self[name]
        return super(_Provider, self).__getattribute__(name)

    def __setattr__(self, name, value):
        raise AttributeError


_var_providers = {}


def register_template_vars(callback, prefix='oo'):
    providers = _var_providers.setdefault(prefix, [])
    providers.append(callback)


def _cp_vars():
    ''' CherryPy data access in template layer
    '''
    return {
        'session': cherrypy.session,
        'request': cherrypy.request,
        'config': utils.config,
    }


def _py_vars():
    ''' Utility functions for template layer
    '''
    return {
        'url': utils.url,
        'attrs': utils.attrs,
        'attr_if': utils.attr_if,
        'checker': lambda e: utils.attr_if('checked', e),
        'selector': lambda e: utils.attr_if('selected', e),
        'readonly': lambda e: utils.attr_if('readonly', e),
        'disabled': lambda e: utils.attr_if('disabled', e),
    }

register_template_vars(_cp_vars, 'cp')
register_template_vars(_py_vars, 'py')

def _get_vars():

    try:
        return cherrypy.request._terp_template_vars
    except:
        pass

    cherrypy.request._terp_template_vars = _vars = {}

    for prefix, cbs in _var_providers.iteritems():
        if prefix:
            provider = _Provider()
            for cb in cbs:
                provider.update(cb())
            _vars[prefix] = provider
        else:
            for cb in cbs:
                _vars.update(cb())
    return _vars

def render_template(template, kw):

    assert isinstance(template, Template), "Invalid template..."

    kw.update(_get_vars())

    # XXX mako overrides 'context' template variable...
    if 'context' in kw:
        kw['ctx'] = kw.pop('context')

    return utils.NoEscape(template.render_unicode(**kw))


def expose(format='html', template=None, content_type=None, allow_json=False, methods=None, mark_only=False):
    """
    :param format: the response's format. Currently understood formats are "json" and "jsonp",
                   any other format is ignored
    :type format: str

    :param template: the path to the template to render (for format=html), from the template search path
                     (. or ./addons), should be defined absolutely (starting with a "/")
    :type template: str

    :param content_type: the Content-Type to force on the resource being returned
    :type content_type: str

    :param allow_json: Specify whether the view should return JSON data instead of rendering the specified template
                       if a `allow_json` GET parameter is specified (should not be used, we will probably end up
                       doing that via the Accept header instead, cleaner)
    :type allow_json: bool

    :param methods: An iterable of HTTP method names allowed to request on this method
    :type methods: [String]

    :param mark_only: Only marks the method as being exposed, of interest mainly for controllers extensions
                      (otherwise the extended/overridden method is not found by CherryPy, this will go away
                      if we ever switch to a routes-based dispatcher)
    :type mark_only: bool
    """
    if methods is not None:
        assert isinstance(methods, (list, tuple))
        methods = tuple([m.upper() for m in methods])

    def expose_wrapper(func):
        if mark_only:
            func.exposed = True
            return func
        def func_wrapper(*args, **kw):
            if methods and cherrypy.request.method.upper() not in methods:
                raise cherrypy.HTTPError(405)

            res = func(*args, **kw)

            if format == 'json' or (allow_json and 'allow_json' in cherrypy.request.params):
                cherrypy.response.headers['Content-Type'] = 'text/javascript'
                return simplejson.dumps(res)
            elif format == 'jsonp' and 'callback' in cherrypy.request.params:
                cherrypy.response.headers['Content-Type'] = 'text/javascript'
                return '%(function)s(%(data)s);' % {
                        'function': cherrypy.request.params['callback'],
                        'data': simplejson.dumps(res)
                    } 

            cherrypy.response.headers['Content-Type'] = content_type or \
            cherrypy.response.headers.get('Content-Type', 'text/html')

            if isinstance(res, dict):

                try:
                    _template = load_template(res['cp_template'])
                except:
                    _template = load_template(template)

                if _template:

                    from openobject.widgets import Widget, OrderedSet
                    from openobject.widgets import js_i18n

                    res['widget_css'] = css = OrderedSet()
                    res['widget_javascript'] = js = {}

                    jset = js.setdefault('head', OrderedSet())
                    jset.add_all([js_i18n])

                    for value in res.itervalues():

                        if isinstance(value, Widget):
                            css.add_all(value.retrieve_css())
                            for script in value.retrieve_javascript():
                                jset = js.setdefault(script.location or 'head', OrderedSet())
                                jset.add(script)

                    return render_template(_template, res).encode("utf-8")

            if not isinstance(res, basestring):
                return unicode(res).encode("utf-8")

            return res

        return utils.decorated(func_wrapper, func, exposed=True)

    return expose_wrapper


# vim: ts=4 sts=4 sw=4 si et
