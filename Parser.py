#coding=utf-8
from collections import namedtuple
Node = namedtuple("Node",["name","rest"])
class Abort(Exception): pass
def Expected(s : str):
    raise Abort( f'\033[0;31;43mError: {s} Expected. \033[0m')
class Parser(object):
    def __init__(self,keys):
        self.keys = keys
    def unpack(self,toks):
        if toks == []:
            Expected("PackNil")
        return toks[0],toks[1:]
    def strip(self,tok,toks):
        t,ts = self.unpack(toks)
        if tok == t:
            return ts
        else:
            Expected(f"Strip '{t}' not match '{tok}'")
    def getid(self,toks):
        t,ts = self.unpack(toks)
        if not t.isdigit() and t not in self.keys:
            return (t,ts)
        else:
            Expected(f"Id '{t}' is num or {self.keys} have '{t}'")
    def getnum(self,toks):
        t,ts = self.unpack(toks)
        if t.isdigit():
            return (int(t),ts)
        else:
            Expected(f"Num '{t}' not is number")
    def expr(self,toks):
        raise NotImplementedError
    def read(self,inp):
        out,rest = self.expr(inp)
        if rest:
            Expected(f"not all parser {rest}")
        return out

__all__ = ["Parser","Node",
           "Abort","Expected"]
