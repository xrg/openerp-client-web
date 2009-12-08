#!/bin/bash

test -f 'populate.sh' || exit

function install {
    test $2 || PYTHONPATH=. easy_install -a -Z -d . $1
}

install "CherryPy>=3.1.2" "-d cherrypy"
install "Babel>=0.9.4" "-d babel"
install "Mako>=0.2.4" "-d mako"
install "simplejson>=2.0.9" "-d simplejson"
install "formencode>=1.2.2" "-d formencode"
install "pyparsing>=1.5.2" "-f pyparsing.py"
install "pytz>=2009j" "-d pytz"
install "xlwt>=0.7" "-d xlwt"

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
