#!/bin/sh

gunicorn -e "PIXYWERK_CONFIG=/home/production/conf/pixyfoo.conf" --pythonpath "/home/production/pixywerk/" --pythonpath "/home/production/ppcode" pixywerk.wsgi:do_werk
