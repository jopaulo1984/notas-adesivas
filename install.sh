#!/bin/bash

if [ -d "/usr/share/notas-adesivas" ];
then
    rm -R /usr/share/notas-adesivas
    rm /usr/bin/notas-adesivas
fi


$dirnotas="/usr/share/notas-adesivas"

echo "instalando..."
mkdir /usr/share/notas-adesivas
mkdir /usr/share/notas-adesivas/notaslib
cp -R ./codigos/notaslib/ /usr/share/notas-adesivas/
cp ./codigos/notas-adesivas-gui.py /usr/share/notas-adesivas/notas-adesivas-gui.py
cp ./codigos/notaslib/icones/notas-adesivas.ico /usr/share/notas-adesivas/notas-adesivas.ico
ln -s /usr/share/notas-adesivas/notas-adesivas-gui.py /usr/bin/notas-adesivas
chmod 777 /usr/bin/notas-adesivas
chmod 777 /usr/share/notas-adesivas/notas-adesivas.ico
echo "Instalação concluída."


