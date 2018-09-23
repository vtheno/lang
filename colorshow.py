#coding=utf-8
import sys
import re
from Lex import *
def key( s ):
    return f'\033[1;32m{s}\033[0m'
def text( s ):
    return f'\033[1;33m{s}\033[0m'
def symbol( s ):
    return f'\033[1;35m{s}\033[0m'
def select( s ):
    return f'\033[1;0;32m{s}\033[0m'
#print( symbol("Hello World") )
keys = ["if","then","else",
        "let","in",
        "fn",
        "infix","infixr"]
syms = ["=>",":","=","(",",",")","+","-","*","/"]
def fuzzy(inp):
    global keys
    out =  [ ]
    pattern = ".*?".join(inp)
    regex = re.compile(pattern)
    for item in keys:
        match = regex.search(item)
        if match:
            out += [(len(match.group()), match.start(), item)]
    return [x for _, _, x in sorted(out)]
def show( source ):
    global keys,syms
    out = ''
    keywords = keys + syms
    spectab = {
        "=":[">"],
        ":":[":"],
    }
    separators = []#[" ","\n","\t"]
    lex = Lex(spectab,keywords,separators)
    source = lex.Tokenise(source)
    for s in source:
        if s in keys:
            out += key (s)
        elif s in syms:
            out += symbol (s)
        elif s not in [" ","\n","\t"]:
            out += text(s)
        else:
            out += s
    return out
__all__ = ["show","fuzzy","select"]
