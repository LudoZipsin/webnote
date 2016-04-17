#!/usr/bin/env bash

sudo mkdir /opt/lz-webtonote
sudo mv webtonote.py /opt/lz-webtonote
sudo ln -s /opt/lz-webtonote/webtonote.py /usr/local/bin/webtonote
mkdir ~/.config/webtonote
mv settings.json ~/.config/webtonote
mkdir ~/.config/webtonote/plugins

for i in `ls plugins`; do
	mv i ~/.config/webtonote/plugins
done
