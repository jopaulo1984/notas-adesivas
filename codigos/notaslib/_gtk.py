
"""
Verifica e importa as bibliotecas Gtk, Gdk e GObject.
"""

from os import path

try:
    import gi
except ImportError:
    print("Necessário instalação do pacote python-gi")
    exit()

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

try:
    from gi.repository import Gtk, Gdk, GObject
except ImportError:
    print("Necessário instalação do pacote python-gtk")
    exit()
    
try:
    from gi.repository import AppIndicator3 as appind
except ImportError:
    print("Necessário instalação do pacote python-appindicator3")
    exit()

def get_builder():
    builder = Gtk.Builder()
    builder.add_from_file(path.dirname(__file__) + "/notas-adesivas.ui")
    return builder   
    
class GTimer:
    def __init__(self, dt, callback, args=()):
        self.dt = dt
        self.call = callback
    
    def start(self):
        GObject.timeout_add(self.dt, self.call)
