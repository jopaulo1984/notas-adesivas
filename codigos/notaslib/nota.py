
from notaslib._gtk import *
import cairo
#from threading import Timer

cssprovider = Gtk.CssProvider()

class NotaAdesiva:
    
    def __init__(self, index, app):
        
        #=====================
        #    propriedades     
        #=====================
        self.__app = app
        self.index = index
        
        #estilo
        self.__bg = Gdk.Color(250, 240, 100)
        self.__fg = Gdk.Color(20, 20, 20)
        self.__font = "Serif Italic 14"    
        
        #geometria
        self.__bounds = 0, 0, 0, 0
        
        #controle
        self.__iniciando = True      
        self.__timer = None
        self.__pant = 0, 0
        self.__posant = 0, 0
        self.__mdown = False 
        self.__alter_count = 0
        self.__moving = False
        self.__iter_s = 0
        self.__iter_e = 0
        self.__mdown_txtv = False
        
        #=========================
        #          gui           =
        #=========================
        builder       = get_builder()
        self.builder  = builder
        self.winnota  = builder.get_object("winnota")
        self.fixed    = builder.get_object("fixed")
        self.textview = builder.get_object("textview")
        self.bconf    = builder.get_object("btnconf")
        self.blimpa   = builder.get_object("btnlimpanota")
        self.baddnt   = builder.get_object("btnaddnota")
        self.brem     = builder.get_object("btnexit")
        
        self.winnota.set_property("name", "winnota" + str(index))
        self.textview.set_property("name", "textview" + str(index))
        
        self.texttag  = self.textview.get_buffer().create_tag("normal")
        self.tagsel   = self.textview.get_buffer().create_tag("selection")
        
        self.winnota.set_gravity(Gdk.Gravity.STATIC)  
        
        self.fixed.set_events( Gdk.EventMask.POINTER_MOTION_MASK |
                               Gdk.EventMask.BUTTON_PRESS_MASK   |
                               Gdk.EventMask.BUTTON_RELEASE_MASK )
        
        #===========================
        #     Conectando sinais    =
        #===========================
        
        self.textview.get_buffer().connect("changed", self._onTextoTrocado) 
        self.winnota.connect("size-allocate", self._onResize)  
        self.fixed.connect("motion-notify-event", self._fixed_mouse_move)
        self.fixed.connect("button-press-event", self._fixed_button_press)
        self.fixed.connect("button-release-event", self._fixed_button_release)
        self.brem.connect("clicked", self._onDeletar)
        self.baddnt.connect("clicked", self._onNovo)
        self.blimpa.connect("clicked", self._onLimpar)
        self.bconf.connect("clicked", self._on_config_win)  
        
        #
        self.winnota.show_all()  
        
    
        self.defCorFundo(Gdk.Color(65300, 60000, 20000))
        self.defFonte("Serif Italic 14", Gdk.Color(2000, 2000, 2000))       
        
        self.__iniciando = False
    
    def _onTextoTrocado(self, w): 
        self._apply_tag_()   
        self._do_alter()
    
    def _onNovo(self, w):
        self.__app.novaNota()
    
    def _onDeletar(self, w):
        self.__app.deletarNota(self)
    
    def _onLimpar(self, w):
        self.textview.get_buffer().set_text("")    
    
    def _onTimeTick(self):
        self.__alter_count -= 1
        if self.__alter_count == 0 :
            self.__app.salvarNotas() 
            self.__timer = None
            print("Salvo!")
        else:
            self.__timer = GTimer(1, self._onTimeTick)
            self.__timer.start()  
    
    def _on_config_win(self, w):
        self.__app.abrirConfiguracao(self)
    
    def _do_alter(self):
        self.__alter_count += 1
        if not self.__timer:
            self.__timer = GTimer(1000, self._onTimeTick)
            self.__timer.start()   
       
    def obtTexto(self):
        buffer = self.textview.get_buffer()
        s = buffer.get_start_iter()
        e = buffer.get_end_iter()       
        return buffer.get_text(s, e, True)
    
    def obtFonte(self):
        """Retorna uma string contendo a fonte."""
        return self.__font #texttag.get_property("font")
    
    def obtCorFonte(self):
        """Retorna um Gdk.Color()"""
        return self.__fg #texttag.get_property("foreground-gdk")
    
    def obtCorFundo(self):
        """Retorna um Gdk.Color()"""
        return self.__bg #estilo.get_background_color(0)
    
    def defTexto(self, texto):      
        self.textview.get_buffer().set_text(texto)        
    
    def defFonte(self, font, fg):
        self.__font = font
        self.__fg = fg    
        self.texttag.set_property("font", self.__font)        
        self.texttag.set_property("foreground-gdk", self.__fg)  
        self._apply_tag_()
        self.__app.salvarNotas()
    
    def defCorFundo(self, bg):     
        
        self.__bg = bg
                
        M = 65535 / 255
        
        provider = Gtk.CssProvider()
        
        provider.load_from_data((\
            "#" + self.textview.get_property("name") + \
            ",#" + self.winnota.get_property("name") + \
            """{
                background-color: rgb( """ + str(int(bg.red/M)) + "," + \
            str(int(bg.green/M)) + "," + str(int(bg.blue/M)) + """);
            }
            """).encode())
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        self.baddnt.modify_bg(Gtk.StateType.NORMAL, self.__bg)
        self.bconf.modify_bg(Gtk.StateType.NORMAL, self.__bg)
        self.blimpa.modify_bg(Gtk.StateType.NORMAL, self.__bg)
        self.brem.modify_bg(Gtk.StateType.NORMAL, self.__bg)        
        
        self.__app.salvarNotas()
        
    def defLimites(self, left, top, width, height):
        """Define os limites da nota."""
        b = left, top, width, height
        if b == self.__bounds: 
            return
        self.__bounds = b
        self.winnota.resize(width, height)
        self.winnota.move(left, top)
    
    def _apply_tag_(self):        
        buffer = self.textview.get_buffer()
        s = buffer.get_start_iter()
        e = buffer.get_end_iter()     
        buffer.apply_tag_by_name("normal", s, e)
            
    # movimento da nota adesiva
    def _fixed_mouse_move(self, w, event):
        if not event: return
        if self.__mdown:
            x, y = self.__pant
            dx, dy = event.x_root - x, event.y_root - y
            rx, ry = self.__posant
            self.winnota.move(rx + dx, ry + dy)
            self.__moving = True
    
    def _fixed_button_press(self, w, event):
        if not event: return
        self.__mdown = True
        self.__pant = event.x_root, event.y_root
        self.__posant = self.winnota.get_position()

    def _fixed_button_release(self, w, event):
        if not event: return
        self.__mdown = False
        if self.__moving: self._do_alter()
        self.__moving = False
    #
    def _onResize(self, w, s):
        b = s.x, s.y, s.width, s.height
        if b == self.__bounds: 
            return
        self.__bounds = b
        self._do_alter()
        #self.__app.salvarNotas()
    
    

