#!/bin/sh

function clean_kid {
    sed -i 's/\t/    /g' $1;    # remove tabs
    sed -i 's/\s*$//g' $1;      # remove trailing spaces
}

function clean_py {
    sed -i 's/\s*$//g' $1;      # remove trailing spaces
}

function clean_source {

    for f in `find -type f -name '*.py'`
    do
        clean_py $f
    done

    for f in `find -type f -name '*.kid'`
    do
        clean_kid $f
    done
}

function clean_bakups {
    find -type f -name '*.pyc' -exec rm -f {} ';'
    find -type f -name '*.bak' -exec rm -f {} ';'
    find -type f -name '*~' -exec rm -f {} ';'
}

case $1 in
    -source) clean_source ;;
    *) clean_bakups ;;
esac
