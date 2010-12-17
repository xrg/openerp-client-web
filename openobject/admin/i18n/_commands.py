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

import os

from babel.messages.frontend import CommandLineInterface
from babel.support import Translations

from openobject.admin import BaseCommand

from openobject import paths


def _get_modules(modules):
    """Get iterator of tuples of all the available addons with first item is
    addon name and second item is full path to the addon.
    """
    if modules.upper() == "ALL":
        modules = os.listdir(paths.addons())
    else:
        modules = modules.split(",")

    for module in modules:
        d = paths.addons(module)
        if os.path.isfile(os.path.join(d, '__openerp__.py')):
            yield module, d


def _get_locales(path, locale=None):
    """Returns an iterator of all locales provided by the addon at 
    the given path.
    
    :param path: the path the an addon
    :param locale: comma separated list of locales or None to get all
                   the locales
    :returns: an iterator of locales
    """
    if locale:
        for l in locale.split(","):
            yield l
            
    if os.path.exists(os.path.join(path, 'po', 'messages')):
        for f in os.listdir(os.path.join(path, 'po', 'messages')):
            if f.endswith('.po'):
                yield f[:-3]

class BabelCommand(BaseCommand):

    name = "i18n"
    description = "i18n commands"

    def __init__(self):
        super(BabelCommand, self).__init__()
        self.cmd = CommandLineInterface()
        self._args = ["", "-q"]

    def execute(self, command, *args, **kw):

        args = self._args + [command] + list(args)
        for k, v in kw.items():
            args += ['-%s' % k, v]

        self.cmd.run(args)

    def get_files(self, locale, domain, path):

        po = ""
        mo = ""
        pot = ""

        if domain:
            pot = os.path.join(path, 'po', domain, '%s.pot' % domain)

        if locale and domain:
            po = os.path.join(path, 'po', domain, '%s.po' % locale)
            mo = os.path.join(path, 'locale', locale, 'LC_MESSAGES', '%s.mo' % domain)

        return pot, po, mo

    def extract(self, locale, domain, path):

        pot, po, mo = self.get_files(locale, domain, path)

        if not os.path.exists(os.path.join(path, 'po', domain)):
            os.makedirs(os.path.join(path, 'po', domain))

        mappath = os.path.join(os.path.dirname(__file__), "mapping", "%s.cfg" % domain)

        os.chdir(path)

        print "Creating '%s'" % pot
        self.execute("extract", '.', o=pot, F=mappath)

    def compile(self, locale, domain, path):

        if not locale:
            _locales = _get_locales(path, locale)
            for l in _locales:
                self.compile(l, domain, path)
            return

        pot, po, mo = self.get_files(locale, domain, path)

        if not os.path.exists(po):
            return
        
        opath = os.path.dirname(mo)
        if not os.path.exists(opath):
            os.makedirs(opath)

        print "Compiling '%s'" % po
        self.execute("compile", D=domain, l=locale, i=po, o=mo)

        if domain == "javascript":

            try:
                tr = Translations.load(os.path.join(path, 'locale'), [locale], domain)
                messages = tr._catalog
                messages.pop("")
            except Exception, e:
                return

            jspath = os.path.join(path, "static", "javascript", "i18n")
            if not os.path.exists(jspath):
                os.makedirs(jspath)
            jspath = os.path.join(jspath, "%s.js" % locale)

            import simplejson
            messages = simplejson.dumps(messages)

            text = """
// Auto generated file. Please don't modify.
openobject.gettext.update(
%(messages)s
);

""" % dict(messages=messages)

            try:
                fo = open(jspath, 'w')
                fo.write(text)
                fo.close()

                print "Creating '%s'" % jspath

            except Exception, e:
                pass


    def run(self, argv):

        self.parser.add_option("-l", "--locale", dest="locale", help="locale (e.g. en_US, fr_FR)")
        self.parser.add_option("-D", "--domain", dest="domain", help="domain (e.g. messages, javascript)")

        self.parser.add_option("-x", "--extract", dest="x", metavar="ALL", help="extract messages for the given addons")
        self.parser.add_option("-c", "--compile", dest="c", metavar="ALL", help="compile po files for the given addons")

        options, args = self.parser.parse_args(argv)

        m = [o for o in [options.x, options.c] if o]
        if not m:
            self.parser.error("Required one of '--extract, --compile'")

        modules = _get_modules(m[0])
        action = None

        if options.x:
            action = self.extract

        elif options.c:
            action = self.compile

        domains = ["messages", "javascript"]
        if options.domain:
            domains = options.domain.split(",")

        for m, p in modules:
            for d in domains:
                action(options.locale, d, p)
