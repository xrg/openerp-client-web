
import os
import sys

from openerp.commands import BaseCommand


class BabelCommand(BaseCommand):

    name = "i18n"
    description = "i18n commands"

    def init(self, locale, domain, modules):
        modules = modules.split(",")
    
    def extract(self, locale, domain, modules):
        pass
    
    def update(self, locale, domain, modules):
        pass
    
    def compile(self, locale, domain, modules):
        pass
    
    def run(self, argv):

        self.parser.add_option("-l", "--locale", dest="locale", help="locale (e.g. en_US, fr_FR)")
        self.parser.add_option("-D", "--domain", dest="domain", help="domain (e.g. messages, javascript)")

        self.parser.add_option("-a", "--init", dest="a", metavar="ALL", help="create catalogs for the given addons")
        self.parser.add_option("-x", "--extract", dest="x", metavar="ALL", help="extract messages for the given addons")
        self.parser.add_option("-u", "--update", dest="u", metavar="ALL", help="update message catalogs for the given addons")
        self.parser.add_option("-c", "--compile", dest="c", metavar="ALL", help="compile po files for the given addons")

        options, args = self.parser.parse_args(argv)

        if options.a:
            return self.init(options.locale, options.domain, options.a)

        if options.x:
            return self.extract(options.locale, options.domain, options.a)

        if options.u:
            return self.update(options.locale, options.domain, options.a)

        if options.c:
            return self.compile(options.locale, options.domain, options.a)
        
        
