#!/bin/sh

export PIXYWERK_CONFIG=/home/production/conf/pixyfoo.conf
gunicorn --pythonpath "/home/production/pixywerk/" --pythonpath "/home/production/ppcode" pixywerk.wsgi:do_werk
