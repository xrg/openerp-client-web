import os
import sys
from optparse import OptionParser

import cherrypy

from openobject import release


COMMANDS = {}


class _CommandType(type):

    def __new__(cls, name, bases, attrs):

        obj = super(_CommandType, cls).__new__(cls, name, bases, attrs)

        if "name" in attrs:
            COMMANDS[attrs["name"]] = obj

        return obj


class BaseCommand(object):

    __metaclass__ = _CommandType

    def __init__(self):
        self.parser = OptionParser(usage=self.usage)
        self.parser.disable_interspersed_args()

    def run(self, argv):
        pass

    def _get_usage(self):
        return "%%prog %s [options]" % getattr(self, "name", self.__class__.__name__)

    usage = property(lambda self: self._get_usage())


class CommandLine(object):

    def run(self, argv):

        self.parser = OptionParser(usage="%prog command [option]", version="%s" % (release.version))

        self.parser.disable_interspersed_args()
        self.parser.print_help = self._help

        options, args = self.parser.parse_args(argv[1:])

        if not args:
            self.parser.error('incorrect number of arguments')

        cmdname = args[0]
        if cmdname not in COMMANDS:
            self.parser.error('unknown command "%s"' % cmdname)


        return COMMANDS[cmdname]().run(args[1:])

    def _help(self):

        print self.parser.format_help()
        print "Commands:"
        longest = max([len(command) for command in COMMANDS])
        format = "  %%-%ds %%s" % max(8, longest + 1)
        commands = COMMANDS.items()
        commands.sort()
        for name, command in commands:
            print format % (name, command.description)


def main():
    CommandLine().run(sys.argv)

