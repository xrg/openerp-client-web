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

import random, time
import binascii

from openobject import tools
from openerp import utils

from openerp.utils import rpc
from openerp.utils import icons
from openerp.utils import cache
from openerp.utils import TempFileName

from openerp import validators

from openerp.widgets import TinyInputWidget
from openerp.widgets import register_widget


__all__ = ["Binary", "Image"]


class Binary(TinyInputWidget):
    template = "/openerp/widgets/form/templates/binary.mako"
    params = ["name", "text", "readonly", "filename", "bin_data", 'value_bin_size', 'val']

    text = None
    file_upload = True
    val = True

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
        try:
            binascii.a2b_base64(value)
        except:
            self.val = False
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
    width = None
    height = None
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
            self.src = tools.url('/openerp/form/binary_image_get_image', model=self.model, id=self.id, field=self.field, nocache=random.randint(0,2**32))
            self.height = attrs.get('img_height', attrs.get('height', None))
            self.width = attrs.get('img_width', attrs.get('width', None))
            self.validator = validators.Binary()
        else:
            self.src =  icons.get_icon(icon)
        if self.readonly:
            self.editable = False

register_widget(Image, ["image", 'picture'])

# vim: ts=4 sts=4 sw=4 si et
