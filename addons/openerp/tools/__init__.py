
import rpc
from tools import *

from openobject.tools import register_template_vars

def _root_vars():
    return {
        'rpc': rpc,
    }

register_template_vars(_root_vars, None)

del register_template_vars

