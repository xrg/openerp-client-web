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
import copy

from openerp.controllers import SecuredController
from openerp.utils import rpc, cache, common, TinyDict

from openobject.tools import expose


#change 'en' to false for context
def adapt_context(val):
    if val == 'en_US':
        return False
    else:
        return val

class Translator(SecuredController):

    _cp_path = "/openerp/translator"

    @expose(template="/openerp/controllers/templates/translator.mako")
    def index(self, translate='fields', **kw):
        params, data = TinyDict.split(kw)
        
        ctx = dict((params.context or {}), **rpc.session.context)
        params['context'] = ustr(ctx)

        proxy = rpc.RPCProxy('res.lang')

        lang_ids = proxy.search([('translatable', '=', '1')])
        langs = proxy.read(lang_ids, ['code', 'name'])

        proxy = rpc.RPCProxy(params.model)

        data = []
        view = []

        view_view = cache.fields_view_get(params.model, False, 'form', ctx, True)

        view_fields = view_view['fields']
        view_relates = view_view.get('toolbar')

        names = view_fields.keys()
        names.sort(lambda x,y: cmp(view_fields[x].get('string', ''), view_fields[y].get('string', '')))

        if translate == 'fields' and params.id:
            for name in names:
                attrs = view_fields[name]
                if attrs.get('translate'):
                    value = {}
                    for lang in langs:
                        context = copy.copy(ctx)
                        context['lang'] = adapt_context(lang['code'])

                        val = proxy.read([params.id], [name], context)
                        val = val[0]

                        value[lang['code']] = val[name] or None

                    data += [(name, value, None, attrs.get('string'))]

        if translate == 'labels':
            for name in names:
                attrs = view_fields[name]
                if attrs.get('string'):
                    value = {}
                    for lang in langs:
                        code=lang['code']
                        val = proxy.read_string(False, [code], [name])

                        if name in val[code]:
                            value[code] = val[code][name] or None

                    if value: data += [(name, value, None, None)]

        if translate == 'relates' and view_relates:
            for bar, tools in view_relates.items():
                for tool in tools:

                    value = {}
                    for lang in langs:
                        code = lang['code']
                        val = rpc.session.execute('object', 'execute', tool['type'], 'read', [tool['id']], ['name'], {'lang': code})

                        value[code] = val[0]['name'] or None

                    data += [(tool['id'], value, tool['type'], None)]

        if translate == 'view':
            for lang in langs:
                code=lang['code']
                view_item_ids = rpc.session.execute('object', 'execute', 'ir.translation', 'search', [('name', '=', params.model), ('type', '=', 'view'), ('lang', '=', code)])
                view_items = rpc.session.execute('object', 'execute', 'ir.translation', 'read', view_item_ids, ['src', 'value'])

                values = []
                for val in view_items:
                    values += [val]

                if values:
                    view += [(code, values)]

        return dict(translate=translate, langs=langs, data=data, view=view, model=params.model, id=params.id, ctx=params.context)

    @expose()
    def save(self, translate='fields', **kw):
        params, data = TinyDict.split(kw)
        
        ctx = dict((params.context or {}), **rpc.session.context)
        params['context'] = ustr(ctx)

        if translate == 'fields':
            if not params.id:
                raise common.message(_("You need to save the resource before adding translations."))

            for lang, value in data.items():

                context = copy.copy(ctx)
                context['lang'] = adapt_context(lang)

                for name, val in value.items():
                    if isinstance(val, basestring):
                        val = [val]

                    for v in val:
                        rpc.session.execute('object', 'execute', params.model, 'write', [params.id], {name : v}, context)

        if translate == 'labels':
            for lang, value in data.items():
                for name, val in value.items():
                    rpc.session.execute('object', 'execute', params.model, 'write_string', False, [lang], {name: val})

        if translate == 'relates':
            for lang, value in data.items():
                for name, val in value.items():
                    rpc.session.execute('object', 'execute', params.models[name], 'write', [int(name)], {'name': val}, {'lang': lang})

        if translate == 'view':
            for lang, value in data.items():
                for id, val in value.items():
                    rpc.session.execute('object', 'execute', 'ir.translation', 'write', [int(id)], {'value': val})

        return self.index(translate=translate, _terp_model=params.model, _terp_id=params.id, ctx=params.context)

# vim: ts=4 sts=4 sw=4 si et
