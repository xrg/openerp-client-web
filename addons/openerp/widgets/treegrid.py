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

import simplejson

from openerp.widgets import TinyWidget
from openobject.widgets import JSLink


class TreeGrid(TinyWidget):

    template = "/openerp/widgets/templates/treegrid.mako"
    params = ['headers', 'showheaders', 'expandall', 'linktarget',
    'onselection', 'onbuttonclick', 'onheaderclick', 'url', 'url_params']

    javascript = [JSLink("openerp", "javascript/treegrid.js")]

    def __init__(self, name, model, headers, url, field_parent=None, ids=[], domain=[], context={}, **kw):

        super(TreeGrid, self).__init__(name=name, model=model, url=url, **kw)

        self.ids = ids or []
        self.domain = domain or []
        self.context = context or {}
        self.headers = simplejson.dumps(headers)

        fields = [field['name'] for field in headers]
        icon_name = headers[0].get('icon')

        params = dict(model=model,
                          ids=ids or '',
                          fields=ustr(fields),
                          domain=ustr(domain),
                          context=ustr(context),
                          field_parent=field_parent,
                          icon_name=icon_name)

        params.update(**kw)
        params.pop('children', None)
        params.pop('parent', None)

        self.showheaders = params.pop('showheaders', 1)
        self.onselection = params.pop('onselection', '')
        self.onbuttonclick = params.pop('onbuttonclick', '')
        self.onheaderclick = params.pop('onheaderclick', '')
        self.expandall = params.pop('expandall', 0)
        self.linktarget = params.pop('linktarget', 0)

        def _jsonify(obj):

            for k, v in obj.items():
                if isinstance(v, dict):
                    obj[k] = _jsonify(v)

            return simplejson.dumps(obj)

        self.url_params = _jsonify(params)

# vim: ts=4 sts=4 sw=4 si et
