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
# -   All names, links and logos of Tiny, Open ERP and Axelor must be
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
            
import base64
import tempfile

from openerp import icons
from openerp import tools
from openerp import cache

from openerp import rpc

from openerp import validators
from openerp.widgets.interface import TinyInputWidget


class Binary(TinyInputWidget):
    template = "templates/binary.mako"
    params = ["name", "text", "readonly", "filename"]

    text = None
    file_upload = True

    def __init__(self, **attrs):
        super(Binary, self).__init__(**attrs)
        self.validator = validators.Binary()
        self.onchange = "onChange(this); set_binary_filename(this, '%s');" % (self.filename or '')

    def set_value(self, value):
        #XXX: server bug work-arround
        try:
            self.text = tools.get_size(value)
        except:
            self.text = value or ''
            

class Image(TinyInputWidget):

    template = "templates/image.mako"

    params = ["src", "width", "height", "model", "id", "field", "stock"]
    src = ""
    width = 32
    height = 32
    field = ''
    stock = True

    def __init__(self, **attrs):
        icon = attrs.get('name')
        attrs['name'] = attrs.get('name', 'Image').replace("-","_")

        super(Image, self).__init__(**attrs)

        self.filename = attrs.get('filename', '')

        if 'widget' in attrs:
            self.stock = False
            self.field = self.name.split('/')[-1]
            self.src = tools.url('/image/get_image', model=self.model, id=self.id, field=self.field)
            self.height = attrs.get('img_height', attrs.get('height', 160))
            self.width = attrs.get('img_width', attrs.get('width', 200))
            self.validator = validators.Binary()
        else:
            self.src =  icons.get_icon(icon)
            

@cache.memoize(1000, force=True)
def get_temp_file(m, n, i):
    t, fn = tempfile.mkstemp()
    return fn


class Picture(TinyInputWidget):
    template = """<div style="text-align: center;">
    <img id="${name}" width="${width}" heigth="${height}" src="${url}"/>
    </div>
    """

    params = ["url", "width", "height"]
    width = 32
    height = 32

    def __init__(self, **attrs):
        super(Picture, self).__init__(**attrs)
        
        self.height = attrs.get('img_height', attrs.get('height', 160))
        self.width = attrs.get('img_width', attrs.get('width', 200))
        self.validator = validators.Binary()
        
        ctx = rpc.session.context.copy()
        ctx.update(self.context or {})
        ctx['bin_size'] = False
        
        proxy = rpc.RPCProxy(self.model)
        
        if not self.id:
            value = proxy.default_get([self.name], ctx)
        else:
            value = proxy.read([self.id], [self.name], ctx)[0]
            
        value = value.get(self.name) or (None, None)

        if isinstance(value, (tuple, list)) and len(value)==2:
            type, data = value
        else:
            type, data = None, value
            
        if data:
            if type == 'stock':
                stock, size = data
                self.url =  icons.get_icon(stock)
            else:
                fname = get_temp_file(str(self.model), str(self.name), str(self.id))
                try:
                    tmp = open(fname, "w")
                    try:
                        tmp.write(base64.decodestring(data))
                    finally:
                        tmp.close()
                except Exception, e:
                    raise
                
                self.url = tools.url("/image/get_picture", model=self.model, name=self.name, id=self.id)
        else:
            self.url = tools.url("/static/images/blank.gif")


# vim: ts=4 sts=4 sw=4 si et

