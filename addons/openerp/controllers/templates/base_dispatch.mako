<%! import cherrypy, pprint
def get_base_template():
    if cherrypy.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return '/openerp/controllers/templates/xhr.mako'
    else:
        return '/openerp/controllers/templates/base.mako'

%>
<%inherit file="${get_base_template()}"/>
