#coding: utf8

"""Lança o ícone indicador no painel do sistema."""

import sys
import os.path

from notaslib._gtk import *

ICONE = "/icones/tryicon.svg"

class Indicador:
    def __init__(self, app):
        self.__app = app
        self.__indi = appind.Indicator.new("notas-adesivas", app.getDir() + ICONE, appind.IndicatorCategory.OTHER)
        self.__indi.set_status(appind.IndicatorStatus.ACTIVE)
        builder = get_builder()
        builder.get_object("mennovo").connect("activate", lambda w: self._onAdcNota())
        builder.get_object("mensair").connect("activate", lambda w: self._onSair())   
        self.__indi.set_menu(builder.get_object("menu"))     
    
    def _onAdcNota(self):
        self.__app.novaNota()
    
    def _onSair(self):
        self.__app.sair()