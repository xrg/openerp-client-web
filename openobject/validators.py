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
import formencode

__all__ = ['BaseValidator', 'DefaultValidator', 'Schema']

class BaseValidator(formencode.api.FancyValidator):
    pass


class DefaultValidator(BaseValidator):
    pass


class Schema(formencode.schema.Schema):
    """Modified Schema validator.

    A schema validates a dictionary of values, applying different validators
    (by key) to the different values.

    This modified Schema allows fields that do not appear in the fields
    parameter of your schema, but filters them out from the value dictionary.
    You might want to set filter_extra_fields to True when you're building a
    dynamic form with unpredictable keys and need these values.

    """

    filter_extra_fields = True
    allow_extra_fields = True
    if_key_missing = None

    def from_python(self, value, state=None):
        # The Schema shouldn't do any from_python conversion because
        # adjust_value already takes care of that for all children.
        return value
