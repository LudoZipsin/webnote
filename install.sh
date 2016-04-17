#!/usr/bin/env bash

sudo mv webtonote.py /usr/local/bin/webtonote
mkdir ~/.config/webtonote
mv settings.json ~/.config/webtonote
mkdir ~/.config/webtonote/plugins
mv plugins/* ~/.config/webtonote/plugins
