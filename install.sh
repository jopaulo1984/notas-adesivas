#!/bin/bash

sh uninstall.sh

$dirnotas="/usr/share/notas-adesivas"

echo "instalando..."
mkdir /usr/share/notas-adesivas
mkdir /usr/share/notas-adesivas/notaslib
cp -R ./codigos/notaslib/ /usr/share/notas-adesivas/
cp ./codigos/notas-adesivas-gui.py /usr/share/notas-adesivas/notas-adesivas-gui.py
cp ./codigos/notaslib/icones/notas-adesivas.ico /usr/share/notas-adesivas/notas-adesivas.ico
cp ./notas-adesivas-gui.desktop /usr/share/applications/notas-adesivas-gui.desktop
cp ./notas-adesivas-gui.desktop ~/.config/autostart/notas-adesivas-gui.desktop
ln -s /usr/share/notas-adesivas/notas-adesivas-gui.py /usr/bin/notas-adesivas
chmod 777 /usr/bin/notas-adesivas
chmod 777 /usr/share/notas-adesivas/notas-adesivas.ico
chmod 777 ~/.config/autostart/notas-adesivas-gui.desktop
echo "Instalação concluída."
