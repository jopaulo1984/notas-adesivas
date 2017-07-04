
import re

def substring(strin, start, end):
    temp = ""
    for i in range(start, end):
        temp += strin[i]
    return temp

def expreg(strin, exp):
    m = re.compile(exp).search(strin)
    if m: return substring(m.string, m.start(), m.end())
    else: return ""

def get_match(strin, exp):
    return re.compile(exp).search(strin)
#

class TagedText():
    def __init__(self, texto=""):
        self.__text = texto
        
    def get_text(self):
        return self.__text
    
    def set_text(self, text):
        self.__text = text
        
    def get_tag_content(self, tag):
        saida = expreg(self.__text, r'\<' + tag + '\>[\w\W\n]*\<\/' + tag + '\>')
        if len(saida) == 0: return ""
        match = get_match(saida, r'\<' + tag + '\>')
        saida = substring(saida, match.end(), len(saida))
        match = get_match(saida, r'\<\/' + tag + '\>')
        saida = substring(saida, 0, match.start())
        return saida
    
    def get_tags_array(self, tag):        
        def _get_next_(saida, strin, tg):
            m = get_match(strin, r'\<' + tg + '\>[\w\W\n]*?\<\/' + tg + '\>')
            if not m: return
            l = len(strin)
            saida.append(substring(strin, m.start(), m.end()))
            if m.start() < l:
                _get_next_(saida, substring(strin, m.end(), l), tg)
        
        saida = []
        _get_next_(saida, self.get_text(), tag)
        return saida
#