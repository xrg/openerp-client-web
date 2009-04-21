#!/bin/sh

test -f 'populate.sh' || exit
test ! -d 'cherrypy' || exit

PYTHONPATH=. easy_install -a -Z -d . "CherryPy>=3.1.2"
PYTHONPATH=. easy_install -a -Z -d . "Babel>=0.9.4"
PYTHONPATH=. easy_install -a -Z -d . "Mako>=0.2.4"
PYTHONPATH=. easy_install -a -Z -d . "simplejson >= 2.0.9"
PYTHONPATH=. easy_install -a -Z -d . "formencode>=1.2.2"

for egg in *.egg
do
    if test -d $egg 
    then
        rm -rf $egg/EGG-INFO
        mv $egg/* .
        rm -rf $egg
    fi
done

rm -f site.*
rm -f easy-install.pth
