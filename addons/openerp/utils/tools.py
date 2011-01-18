###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import __builtin__
import collections

import datetime
import os
import time
import tempfile

from dateutil.relativedelta import relativedelta

import rpc

class BuiltinOrFalseDefaultDict(collections.defaultdict):
    """ If a value is missing, from the dict, tries to get it from the
     builtins and defaults to `False` if still none available.

     Base `defaultdict` is called during builtins resolution and will return
    `False` instead of whatever default we need (e.g. `True`) so it does not
    work when we need access to the builtins
    """
    def __init__(self, *args, **kwargs):
        # Python 2.5 (and 2.6.1)'s defaultdict blows up when None as first
        # arg (requires callable) so initialize in two steps
        super(BuiltinOrFalseDefaultDict, self).__init__()
        self.update(*args, **kwargs)
    def __missing__(self, key):
        # module-global __builtins__ can be a dict or a module depending on
        # the context. __builtin__ is a safer bet: always a module
        return getattr(__builtin__, key, False)

def expr_eval(string, context=None):
    context = BuiltinOrFalseDefaultDict(
            context or {},
            uid=rpc.session.uid,
            current_date=time.strftime('%Y-%m-%d'),
            time=time,
            datetime=datetime,
            relativedelta=relativedelta)
    if isinstance(string, basestring):
        evaled = eval(string, context)
        if isinstance(evaled, list):
            # eval'd a domain, re-eval it with active_id replacement
            return eval(string.replace("'active_id'", "active_id"), context)
        # Anything else (e.g. context), just return it
        return evaled

    else:
        if isinstance(string, dict):
            for i,v in string.items():
                if v=='active_id':
                    string[i] = eval(v,context)
                elif v==['active_id']:
                    string[i] = eval(v[0],context)
        return string

def node_attributes(node):
    attrs = node.attributes
    
    if not attrs:
        return {}
    # localName can be a unicode string, we're using attribute names as
    # **kwargs keys and python-level kwargs don't take unicode keys kindly
    # (they blow up) so we need to ensure all keys are ``str``
    return dict([(str(attrs.item(i).localName), attrs.item(i).nodeValue)
                 for i in range(attrs.length)])

def xml_locate(expr, ref):
    """Simple xpath locator.

    >>> xml_locate("/form[1]/field[2]", doc)
    >>> xml_locate("/form[1]", doc)

    @param expr: simple xpath with tag name and index
    @param ref: reference node

    @return: list of nodes
    """

    if '/' not in expr:
        name, index = expr.split('[')
        index = int(index.replace(']', ''))

        nodes = [n for n in ref.childNodes if n.localName == name]
        try:
            return nodes[index-1]
        except Exception, e:
            return []

    parts = expr.split('/')
    for part in parts:
        if part in ('', '.'):
#            for node in ref.childNodes:
#               if node.nodeType == node.ELEMENT_NODE:
#                   ref = node
            continue
        ref = xml_locate(part, ref)

    return [ref]

def get_xpath(expr, pn):
    
    """Find xpath.

    >>> get_xpath("/form/group[3]/notebook/page[@string:'Extra Info']/field[@name='progress'], doc)
    >>> get_xpath("/form", doc)
    @param expr: xpath with tag name, index, string and name attributes suported
    @param pn: reference node

    @return: list of nodes
    """
    
    if '/' not in expr:
        name = expr
        param = None
        index = None
        
        if '[' in expr:
            name, param = expr.split('[')
            try:
                index = int(param.replace(']', ''))
            except:
                param = param.replace(']', '')
                if param and '@' in param:
                    param = param.strip('@')
                    key = param.split('=')[0]
                    value = param.split('=')[1][1:-1]
                    
        if index:
            nodes = [n for n in pn.childNodes if n.localName == name]
            try:
                return nodes[index-1]
            except:
                return []
            
        for child in pn.childNodes:
            if child.localName and child.localName == name:
                if param and key in child.attributes.keys():
                    if child.getAttribute(key) == value:
                        return child
                else:
                    return child
        return False
    
    parts = expr.split('/')
    for part in parts:
        if part in ('', '.'):
            continue
        n = get_xpath(part, pn)
        if n:
            pn = n
    return [pn]


def get_node_xpath(node):

    pn = node.parentNode
    xp = '/' + node.localName
    root = xp + '[1]'

    if pn and pn.localName and pn.localName != 'view':
        xp = get_node_xpath(pn) + xp

    nodes = [n for n in pn.childNodes if n.localName == node.localName]
    xp += '[%s]' % (nodes.index(node) + 1)

    return xp

def get_size(sz):
    """
    Return the size in a human readable format
    """
    if not sz:
        return False

    units = ('bytes', 'Kb', 'Mb', 'Gb')
    if isinstance(sz,basestring):
        sz=len(sz)
    s, i = float(sz), 0
    while s >= 1024 and i < len(units)-1:
        s = s / 1024
        i = i + 1
    return "%0.2f %s" % (s, units[i])

def context_with_concurrency_info(context, concurrency_info):
    ctx = (context or {})
    if not concurrency_info:
        return ctx
    if isinstance(concurrency_info, tuple):
        concurrency_info = [concurrency_info]
    return dict(ctx, __last_update=dict(concurrency_info))


class TempFileName(str):
    '''A string representing a temporary file name that will be deleted when object is deleted'''
    def __new__(cls, suffix="", prefix=tempfile.template, dir=None, text=False):
        fd, fn = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir, text=text)
        os.close(fd)
        return str.__new__(cls, fn)
    
    def __init__(self, *args, **kwargs):
        self.__os_path_exists = os.path.exists
        self.__os_unlink = os.unlink
        str.__init__(self, *args, **kwargs)

    def __del__(self):
        if self.__os_path_exists(self):
            self.__os_unlink(self)

    def __copy__(self):
        return self

    def __deepcopy__(self, visit):
        return self


# vim: ts=4 sts=4 sw=4 si et
