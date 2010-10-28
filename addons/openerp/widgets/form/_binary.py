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
            
import base64
import time

from openobject import tools
from openerp import utils

from openerp.utils import rpc
from openerp.utils import icons
from openerp.utils import cache
from openerp.utils import TempFileName

from openerp import validators

from openerp.widgets import TinyInputWidget
from openerp.widgets import register_widget


__all__ = ["Binary", "Image", "Picture", "get_temp_file", "generate_url_for_picture"]


class Binary(TinyInputWidget):

    template = "/openerp/widgets/form/templates/binary.mako"
    params = ["name", "text", "readonly", "filename", "bin_data", 'value_bin_size']

    text = None
    file_upload = True

    def __init__(self, **attrs):
        super(Binary, self).__init__(**attrs)
        self.validator = validators.Binary()
        self.onchange = "set_binary_filename(this, '%s');" % (self.filename or '')
        self.bin_data = attrs.get('value')
        # if bin_size was in context when reading the binary field, then the field's value is actually the binary
        # field's content size
        self.value_bin_size = getattr(self, 'context', {}).get('bin_size', False)

    def set_value(self, value):
        #XXX: server bug work-arround
        if self.value_bin_size:
            self.text = value
            return
        try:
            self.text = utils.get_size(value)
        except:
            self.text = value or ''

register_widget(Binary, ["binary"])


class Image(TinyInputWidget):

    template = "/openerp/widgets/form/templates/image.mako"

    params = ["src", "width", "height", "model", "id", "field", "stock", 'bin_src']
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
        self.state = attrs.get('state')
        self.field = self.name.split('/')[-1]
        if attrs.get('widget'):
            if self.id:
                self.src = tools.url('/openerp/image/get_image', model=self.model, id=self.id, field=self.field)
            elif attrs.get('value'):
                self.bin_src =attrs['value']
            else:
                self.src =  self.bin_src = ''
            self.height = attrs.get('img_height', attrs.get('height', 65))
            self.width = attrs.get('img_width', attrs.get('width', 200))
            self.validator = validators.Binary()
        else:
            self.src =  icons.get_icon(icon)
        if self.readonly:
            self.editable = False
            
register_widget(Image, ["image"])


@cache.memoize(1000, force=True)
def get_temp_file(**kw):
    return TempFileName()


def generate_url_for_picture(model, name, id, value):
    url = ''

    if isinstance(value, (tuple, list)) and len(value)==2:
        type, data = value
    else:
        type, data = None, value

    if data:
        if type == 'stock':
            stock, size = data
            url =  icons.get_icon(stock)
        else:
            key = "%s,%s:%s@%s" % (model, id or 0, name, time.time())
            hashkey = str(hash(key))
            fname = get_temp_file(hash=hashkey)
            tmp = open(fname, "w")
            try:
                tmp.write(base64.decodestring(data))
            finally:
                tmp.close()

            url = tools.url("/openerp/image/get_picture", hash=hashkey)
    else:
        url = tools.url("/static/images/blank.gif")

    return url


class Picture(TinyInputWidget):
    template = """<div style="text-align: center;">
    <img id="${name}" ${width} ${height} src="${url}" kind="picture"/>
    </div>
    """

    params = ["url", "width", "height"]

    def __init__(self, **attrs):
        super(Picture, self).__init__(**attrs)

        height = attrs.get('img_height', attrs.get('height', None))
        self.height = height and 'height="%s"' % height or ''
        width = attrs.get('img_width', attrs.get('width', None))
        self.width = width and 'width="%s"' % width or ''
        self.validator = validators.Binary()

        ctx = rpc.session.context.copy()
        ctx.update(self.context or {})
        ctx['bin_size'] = False

        proxy = rpc.RPCProxy(self.model)

        if '/' in self.name:
            name = self.name.rsplit('/', 1)[-1]
        else:
            name = self.name

        if not self.id:
            value = proxy.default_get([name], ctx)
        else:
            value = proxy.read([self.id], [name], ctx)[0]

        value = value.get(name) or (None, None)
        self.url = generate_url_for_picture(self.model, name, self.id, value)

register_widget(Picture, ["picture"])


# vim: ts=4 sts=4 sw=4 si et
