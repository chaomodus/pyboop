#!/bin/sh

find -name '*~' |xargs rm
find -name '*.pyc' |xargs rm
if [ -d html ]; then
    rm -r html
fi
if [ -d build ]; then
    rm -r build
fi
if [ -d pyboop.egg-info ]; then
    rm -r pyboop.egg-info
fi
if [ -d dist ]; then
    rm -r dist
fi
