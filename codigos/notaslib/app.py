#coding: utf8

import os

from os import path
from notaslib._gtk import *    
from notaslib.indicador import *
from notaslib.nota import *
from notaslib.strings import *

DIR_NOTAS = path.dirname(path.expanduser("~") + "/.notas-adesivas/")
FILE_NOTAS = DIR_NOTAS + "/notas-adesivas.info"

try:
    os.stat(DIR_NOTAS)
except:
    os.system("mkdir " + DIR_NOTAS)
#========================================

class Aplicativo(Gtk.Application):
    def __init__(self):
        self.editando = True
        Gtk.Application.__init__(self)
        self.__indicador = Indicador(self)
        self.__notas = []
        self.carregarNotas()
        self.editando = False
    
    def obtIndicador(self):
        return self.__indicador

    def obtNotas(self):
        return self.__notas
    
    def _adcNota(self, nota):
        self.__notas.append(nota)
    
    def carregarNotas(self): 
        def to_gdk_color(corv):            
            return Gdk.Color(int(corv[0]), int(corv[1]), int(corv[2]))
        
        if not os.path.exists(FILE_NOTAS) : return
        f = open(FILE_NOTAS, "r")
        tagtext = TagedText(f.read())
        f.close()
        
        i = 1
        for strnt in tagtext.get_tags_array("note"):
            tt = TagedText(strnt)
            left = int(tt.get_tag_content("left"))
            top  = int(tt.get_tag_content("top"))
            width = int(tt.get_tag_content("width"))
            height = int(tt.get_tag_content("height"))
            font  = tt.get_tag_content("font")
            fg = to_gdk_color(tt.get_tag_content("fg").split(","))
            bg = to_gdk_color(tt.get_tag_content("bg").split(","))
            texto = tt.get_tag_content("text")
            nt = NotaAdesiva(i, self)
            nt.defLimites(left, top, width, height)
            nt.defFonte(font, fg)
            nt.defCorFundo(bg)
            nt.defTexto(texto)
            self._adcNota(nt)
            i+=1    
    
    def executar(self):
        Gtk.main()
    
    def salvarNotas(self):
        
        if self.editando:
            return
        
        self.editando = True
        strout = ""
        
        try:        
            for nt in self.__notas:
                px, py = nt.winnota.get_position()
                fg = nt.obtCorFonte()
                bg = nt.obtCorFundo()
                alloc = nt.winnota.get_allocation()
                strout += \
                    "<note>\n" \
                    "  <left>" + str(px) + "</left>\n" \
                    "  <top>" + str(py) + "</top>\n" \
                    "  <width>" + str(alloc.width) + "</width>\n" \
                    "  <height>" + str(alloc.height) + "</height>\n" \
                    "  <font>" + nt.obtFonte() + "</font>\n" \
                    "  <fg>" + str(fg.red) + "," + str(fg.green) + "," + str(fg.blue) + "</fg>\n" \
                    "  <bg>" + str(bg.red) + "," + str(bg.green) + "," + str(bg.blue) + "</bg>\n" \
                    "  <text>"  + nt.obtTexto() + "</text>\n" \
                    "</note>\n"
            
            f = open(FILE_NOTAS, "w")
            f.write(strout)
            f.close()
        except Exception as ex:
            print(ex)
        
        self.editando = False
    
    def sair(self):
        Gtk.main_quit()
        exit()   
    
    def novaNota(self):
        
        def _obt_nota_pelo_indice_(indice):
            for nt in self.__notas: 
                if nt.index == indice: return nt
            return
        
        def _obt_indice_da_nota_():
            i = 1
            while _obt_nota_pelo_indice_(i): i+=1
            return i
        
        nt = NotaAdesiva(_obt_indice_da_nota_(), self)
        self._adcNota(nt)
        #self.salvarNotas()
    
    def deletarNota(self, nota):
        builder = get_builder()
        remdlg = builder.get_object("winremdialog")
        remdlg.set_transient_for(nota.winnota)
        if remdlg.run() == 1: 
            self.__notas = [n for n in self.__notas if nota != n]
            nota.winnota.destroy()
            self.salvarNotas()    
        remdlg.destroy() 
    
    def getDir(self):
        return path.dirname(__file__)

    def abrirConfiguracao(self, nota: NotaAdesiva):
        props = [nota.obtFonte(), nota.obtCorFonte(), nota.obtCorFundo()]
        builder = get_builder()
        winconfig = builder.get_object("winconfig")
        winconfig.set_transient_for(nota.winnota)
        widgets = [builder.get_object("winconfig-btnfonte"),
                   builder.get_object("winconfig-btncorfonte"),
                   builder.get_object("winconfig-btncorfundo")]
        widgets[0].set_font_name(props[0])
        for i in range(1, 3): widgets[i].set_color(props[i])
        if winconfig.run() == 1:            
            nota.defFonte(widgets[0].get_font_name(), widgets[1].get_color())
            nota.defCorFundo(widgets[2].get_color())
        winconfig.destroy()         