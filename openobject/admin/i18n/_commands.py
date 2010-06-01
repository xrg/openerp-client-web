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

import os
import sys
import time

from babel.messages.frontend import CommandLineInterface
from babel.support import Translations

from openobject.admin import BaseCommand


def _get_modules(modules):

    import openobject.addons

    ADDONS_PATH = openobject.addons.ADDONS_PATH

    if modules.upper() == "ALL":
        modules = os.listdir(ADDONS_PATH)
    else:
        modules = modules.split(",")

    for module in modules:
        d = os.path.join(ADDONS_PATH, module)
        if os.path.isfile(os.path.join(d, '__openerp__.py')):
            yield module, os.path.join(d, 'locales')


def _get_locales(path, locale=None):

    if locale:
        for l in locale.split(","):
            yield l

    for d in os.listdir(path):
        if os.path.exists(os.path.join(path, d, 'LC_MESSAGES')):
            yield d

def _make_backup(fpath):

    if os.path.exists(fpath):
        i = 0
        while True:
            i += 1
            npath = '%s.%s.bak' % (fpath, i)
            if not os.path.exists(npath):
                break
        try:
            fo = open(npath, "w")
            try:
                fo.write(open(fpath).read())
            finally:
                fo.close()
        except:
            pass

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
            pot = os.path.join(path, '%s.pot' % domain)

        if locale and domain:
            po = os.path.join(path, locale, 'LC_MESSAGES', '%s.po' % domain)
            mo = os.path.join(path, locale, 'LC_MESSAGES', '%s.mo' % domain)

        return pot, po, mo

    def init(self, locale, domain, path):

        _locales = _get_locales(path, locale)

        for l in _locales:

            pot, po, mo = self.get_files(l, domain, path)

            if os.path.exists(po) or not os.path.exists(pot):
                continue

            print "Creating '%s'" % (po)
            self.execute("init", l=l, D=domain, d=path, i=pot)

    def extract(self, locale, domain, path):

        pot, po, mo = self.get_files(locale, domain, path)

        if not os.path.exists(path):
            os.makedirs(path)

        modpath = os.path.dirname(path)
        mappath = os.path.join(os.path.dirname(__file__), "mapping", "%s.cfg" % domain)

        if domain == "messages" and os.path.basename(modpath) == "base":
            mappath = os.path.join(os.path.dirname(__file__), "mapping", "base.cfg")
            os.chdir(os.path.dirname(os.path.dirname(modpath)))
        else:
            os.chdir(modpath)

        _make_backup(pot)

        print "Creating '%s'" % pot
        self.execute("extract", '.', o=pot, F=mappath)

    def update(self, locale, domain, path):

        if not locale:
            _locales = _get_locales(path, locale)
            for l in _locales:
                self.update(l, domain, path)
            return

        pot, po, mo = self.get_files(locale, domain, path)

        if not os.path.exists(po):
            return

        _make_backup(po)

        print "Updating '%s'" % po
        self.execute("update", "-N", D=domain, l=locale, i=pot, o=po)

    def compile(self, locale, domain, path):

        if not locale:
            _locales = _get_locales(path, locale)
            for l in _locales:
                self.compile(l, domain, path)
            return

        pot, po, mo = self.get_files(locale, domain, path)

        if not os.path.exists(po):
            return

        print "Compiling '%s'" % po
        self.execute("compile", D=domain, l=locale, i=po, o=mo)

        if domain == "javascript":

            try:
                tr = Translations.load(path, [locale], domain)
                messages = tr._catalog
                messages.pop("")
            except Exception, e:
                return

            jspath = os.path.dirname(path)
            jspath = os.path.join(jspath, "static", "javascript", "i18n")
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


    def clean(self, locale, domain, path):

        def walk(p, d, files):
            for f in files:

                if f.endswith(".bak"):
                    f = os.path.join(d, f)
                    os.remove(f)

        os.path.walk(path, walk, None)


    def run(self, argv):

        self.parser.add_option("-l", "--locale", dest="locale", help="locale (e.g. en_US, fr_FR)")
        self.parser.add_option("-D", "--domain", dest="domain", help="domain (e.g. messages, javascript)")

        self.parser.add_option("-a", "--init", dest="a", metavar="ALL", help="create catalogs for the given addons")
        self.parser.add_option("-x", "--extract", dest="x", metavar="ALL", help="extract messages for the given addons")
        self.parser.add_option("-u", "--update", dest="u", metavar="ALL", help="update message catalogs for the given addons")
        self.parser.add_option("-c", "--compile", dest="c", metavar="ALL", help="compile po files for the given addons")
        self.parser.add_option("-k", "--clean", dest="k", action="store_true", help="clean all backup files.")

        options, args = self.parser.parse_args(argv)

        m = [o for o in [options.a, options.x, options.u, options.c, options.k] if o]
        if not m:
            self.parser.error("Reqiored one of '--init, --extract, --update, --compile, --clean'")


        if options.k:
            m = ["all"]

        modules = _get_modules(m[0])
        action = None

        if options.a:
            action = self.init

        elif options.x:
            action = self.extract

        elif options.u:
            action = self.update

        elif options.c:
            action = self.compile

        elif options.k:
            action = self.clean

        domains = ["messages", "javascript"]
        if options.domain:
            domains = options.domain.split(",")

        for m, p in modules:
            for d in domains:
                action(options.locale, d, p)

# vim: ts=4 sts=4 sw=4 si et

