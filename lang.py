#coding=utf-8
from Lex import *
from Parser import *
"""
E = E + E 
  | E - E
  | E * E
  | E / E
  | num
equal
E = E + T | E - T | T      ;; this is left assoc
T = T * F | T / F | F      ;; this is left assoc
F = num
----------
A    =  f1 Aopt | ... | fn Aopt
Aopt =  g1 Aopt | ... | gm Aopt | /\ 
----------
E = T + E | T - E | T      ;; this is right assoc
T = F * T | F / T | F      ;; this is right assoc
F = num
----------
E    = T Eopt
Eopt = + T Eopt | - T Eopt | /\ 
----------
items = ( E rest_item )
rest_item = , E | , | /\ buttom
----------
equal
E = T Eopt
Eopt = + T Eopt | - T Eopt | /\ buttom
T = F Topt
Topt = * F Topt | / F Topt | /\ buttom
F = A Fopt
    Fopt = ( E )  | /\ buttom
equal
level expr
0     A = num | id
1     F = A ( E ) | A
2     T = T * F | T / F | F
3     E = E + T | E - T | T
infix level table
     A = num | id | if | let | fn | tuple | infix
0    F = F * A | F / A | A
1    T = T + F | T - F | F
2    E = E T | E ( T ) | T
"""

class parser(Parser):
    def __init__(self,*args,**kw):
        Parser.__init__(self,*args,**kw)
        self.infix_tab = [ 
            [ [ ]      , [ ] ], # 0
            [ ["*","/"], [ ] ], # 1
            [ ["+","-"], [ ] ], # 2
            [ [ ]      , [ ] ], # 3
            # 4 is expr ,eopt 
        ]
        self.user_infix = [ ]
        self.starts = ["if","let","(","fn","infix","infixr"]
    def defn(self,toks):
        if toks:
            x,xs = self.unpack(toks)
            if x == '(':
                e_var,rest1 = self.ids( xs )
                e_val,rest2 = self.expr( self.strip("=",self.strip(')',rest1)) )
                return ( (e_var,e_val),rest2 )
            else: # if (a,b,c) = 2 then a = b = c = 2 elif (a,b,c) = (1,2,3) then a = 1,b = 2,c = 3
                e_var,rest1 = self.getid( toks )
                e_val,rest2 = self.expr ( self.strip("=",rest1) )
                return ( ([e_var],e_val),rest2 )
        else:
            Expected(f"defn: {toks}")
    def defnopt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t == ',':
                defn2,rest2 = self.defn(ts)
                return self.defnopt( expr + [defn2] , rest2)
        return (expr,toks)
    def defns(self,toks):
        defn1,rest1 = self.defn(toks)
        return self.defnopt( [defn1] , rest1)
    def atom(self,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t == 'if':
                e1,rest1 = self.expr(ts)
                e2,rest2 = self.expr( self.strip("then",rest1) )
                e3,rest3 = self.expr( self.strip("else",rest2) )
                return (Node("If",[e1,e2,e3]),rest3)
            elif t == 'let':
                #e1,rest1 = self.getid( ts ) #self.expr(ts)
                #e2,rest2 = self.expr( self.strip("=",rest1) )
                defns,rest2 = self.defns( ts )
                e3,rest3 = self.expr( self.strip("in",rest2) )
                #print( "let_defns:",defns,"|",e3 )
                return (Node("Let",[defns,e3]),rest3)
            elif t == '(': 
                e_items,rest1 = self.items( ts )
                if len(e_items) == 1:
                    return (Node("Paren",e_items),self.strip(")",rest1))
                return (Node("Tuple",e_items),self.strip(')',rest1))
            elif t == 'fn':
                x,xs = self.unpack(ts)
                if x == '(':
                    evar,rest1 = self.ids( xs )
                    rest1 = self.strip(")",rest1)
                    ebody,rest2 = self.expr( self.strip("=>",rest1) )
                    return (Node("Fn",[evar,ebody]),rest2)
                else:
                    evar,rest1 = self.getid( ts )
                    ebody,rest2 = self.expr( self.strip("=>",rest1) )
                    return (Node("Fn",[[evar],ebody]),rest2)
            elif t == "infix":
                assoc = 0
                len_infix = len(self.infix_tab)
                x,xs = self.unpack(ts)
                if x.isdigit():
                    level,rest1 = self.getnum( ts )
                    if level >= len_infix:
                        Expected(f"max infix level {len_infix - 1} not {level}")
                    symop,rest2 = self.getid( rest1 )
                else:
                    level = 0
                    symop,rest2 = self.getid( ts )
                self.user_infix += [symop]
                self.infix_tab[level][assoc] += [symop]
                return (Node("Infix",[level,assoc,symop]), rest2)
            elif t == "infixr":
                assoc = 1
                len_infix = len(self.infix_tab)
                x,xs = self.unpack(ts)
                if x.isdigit():
                    level,rest1 = self.getnum( ts )
                    if level >= len_infix:
                        Expected(f"max infix level {len_infix - 1} not {level}")
                    symop,rest2 = self.getid( rest1 )
                else:
                    level = 0
                    symop,rest2 = self.getid( ts )
                self.user_infix += [symop]
                self.infix_tab[level][assoc] += [symop]
                return (Node("Infixr",[level,assoc,symop]), rest2)
            elif t.isdigit():
                num,rest1 = self.getnum( toks )
                return (Node("Num",[num]),rest1)
            else:
                var,rest1 = self.getid( toks )
                val = Node("Var",[var])
                return (val,rest1)
        else:
            Expected(f"atom {toks}")
    def ids(self,toks):
        t,ts = self.unpack(toks)
        if t == ")":
            return ([ ],toks)
        else:
            id,rest = self.getid(toks)
            return self.idsopt( [id],rest)
    def idsopt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t == ",":
                e2,rest2 = self.getid(ts)
                return self.idsopt(expr + [e2],rest2)
        return (expr,toks)
    def items(self,toks):
        t,ts = self.unpack(toks)
        if t == ")":
            return ([ ],toks)
        else:
            e1,rest = self.expr(toks)
            return self.itemsopt( [e1],rest)
    def itemsopt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t == ",":
                e2,rest2 = self.expr(ts)
                return self.itemsopt(expr + [e2],rest2)
        return (expr,toks)
    def expr(self,toks):
        e1,rest1 = self.level3(toks)
        return self.eopt(e1,rest1)
    def eopt(self,expr,toks):
        if toks: # level 4
            t,ts = self.unpack(toks)
            if t in self.starts or t not in self.keys:
                es,rest = self.atom(toks)
                return self.eopt(Node("App",[expr,es]),rest)
        return (expr,toks)
    def level3(self,toks):
        e1,rest1 = self.term(toks)
        return self.l3opt(e1,rest1)
    def l3opt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            print( t,3,self.infix_tab[3])
            if t in self.infix_tab[3][0]:
                e2,rest = self.term(ts) 
                return self.l3opt(Node(t,[expr,e2]),rest)
            elif t in self.infix_tab[3][1]:
                e2,rest = self.expr(ts) 
                return self.l3opt(Node(t,[expr,e2]),rest)
        return (expr,toks)
    def term(self,toks):
        e1,rest1 = self.fator(toks)
        return self.topt(e1,rest1)
    def topt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            print( t,2,self.infix_tab[2])
            if t in self.infix_tab[2][0]:
                e2,rest = self.fator(ts) # left assoc  => 1 + 2 + 3 => (1 + 2) + 3 => (+ (+ 1 2) 3)
                return self.topt(Node(t,[expr,e2]),rest)
            elif t in self.infix_tab[2][1]:
                e2,rest = self.expr(ts) # right assoc => 1 + 2 + 3 => 1 + (2 + 3) => (+ 1 (+ 2 3))
                return self.topt(Node(t,[expr,e2]),rest)
        return (expr,toks)
    def fator(self,toks):
        e1,rest1 = self.level0(toks)
        return self.fopt(e1,rest1)
    def fopt(self,expr,toks):
        #print( expr, toks )
        if toks:
            t,ts = self.unpack(toks)
            print( t,1,self.infix_tab[1] )
            if t in self.infix_tab[1][0]:
                e2,rest = self.level0(ts) # left
                return self.fopt(Node(t,[expr,e2]),rest)
            elif t in self.infix_tab[1][1]:
                e2,rest = self.expr(ts) # right 
                return self.fopt(Node(t,[expr,e2]),rest)
        return (expr,toks)
    def level0(self,toks):
        e1,rest1 = self.atom(toks)
        return self.l0opt(e1,rest1)
    def l0opt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            print( t,0,self.infix_tab[0] )
            if t in self.infix_tab[0][0]:
                e2,rest = self.atom(ts) # left
                return self.l0opt(Node(t,[expr,e2]),rest)
            elif t in self.infix_tab[0][1]:
                e2,rest = self.expr(ts) # right 
                return self.l0opt(Node(t,[expr,e2]),rest)            
        return (expr,toks)

keywords = ["if","then","else",
            "let","=","in",
            "fn",
            "infix","infixr",
            "=>",":",
            "(",",",")","+","-","*","/"]
spectab = {
    "=":[">"],
    ":":[":"],
}
separators = [" ","\n","\t"]
lex = Lex(spectab,keywords,separators)
p   = parser(keywords)
parse = p.read

__all__ = ["lex","parse","p"]
# "interpreter","Empty","Extend","enviroment"
# implement a user datatype define
