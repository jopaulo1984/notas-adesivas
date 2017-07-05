#!/bin/bash

su
remove() {
    if [ $1 = "-f" ];
    then
        rm $2
    else
        if [ -d $2 ];
        then
            rm -R $2
        fi
    fi
}

remove "-d" "/usr/share/notas-adesivas"
remove "-f" "/usr/bin/notas-adesivas"
remove "-f" "/usr/share/applications/notas-adesivas-gui.desktop"
exit
remove "-f" "~/.config/autostart/notas-adesivas-gui.desktop"
