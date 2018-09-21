#coding=utf-8
from Lex import *
from Parser import *
class parser(Parser):
    def __init__(self,*args,**kw):
        Parser.__init__(self,*args,**kw)
    def idsopt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t == ',':
                e2,rest2 = self.getid(ts)
                return self.idsopt( expr + [e2],rest2)
        return (expr,toks)
    def getids(self,toks):
        e1,rest1 = self.getid(toks)
        return self.idsopt( [e1] ,rest1 ) # rest is binop 
    def defn(self,toks):
        if toks:
            x,xs = self.unpack(toks)
            if x == '(':
                e_var,rest1 = self.getids( xs )
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
                print( "let_defns:",defns,"|",e3 )
                return (Node("Let",[defns,e3]),rest3)
            elif t == '(': # need parent in there?
                e_items,rest1 = self.items( ts )
                return (Node("Tuple",e_items),self.strip(')',rest1))
            elif t == "[":
                e1,rest1 = self.expr(ts)
                return (Node("Paren",[e1]),self.strip("]",rest1))
            elif t == 'fn':
                # FN = fn <variable> => <expr> 
                x,xs = self.unpack(ts)
                if x == '(':
                    evar,rest1 = self.getids( xs )
                    ebody,rest2 = self.expr( self.strip("=>",self.strip(')',rest1)) )
                    return (Node("Fn",[evar,ebody]),rest2)
                else:
                    evar,rest1 = self.getid( ts )
                    ebody,rest2 = self.expr( self.strip("=>",rest1) )
                    return (Node("Fn",[evar,ebody]),rest2)
            elif t.isdigit():
                num,rest1 = self.getnum( toks )
                return (Node("Num",[num]),rest1)
            else:
                var,rest1 = self.getid( toks )
                return (Node("Var",[var]),rest1)
        else:
            Expected(f"atom {toks}")
    """
    E = E + E 
      | E - E
      | E * E
      | E / E
      | num
    equal
    E = E + T | E - T | T
    T = T * F | T / F | F
    F = num
    items = ( E rest_item )
    rest_item = , E | , | /\ buttom
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
    """
    def expr(self,toks):
        e1,rest1 = self.term(toks)
        return self.eopt(e1,rest1) # rest is binop 
    def eopt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t in ["+","-"]:
                e2,rest = self.term(ts)
                return self.eopt(Node(t,[expr,e2]),rest)
        return (expr,toks)
    def term(self,toks):
        e1,rest1 = self.fator(toks)
        return self.topt(e1,rest1)
    def topt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t in ["*","/"]:
                e2,rest = self.fator(ts)
                return self.topt(Node(t,[expr,e2]),rest)
        return (expr,toks)
    def fator(self,toks):
        e1,rest1 = self.atom(toks)
        return self.fopt(e1,rest1)
    def fopt(self,expr,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t == "(":
                e2,rest = self.atom(toks)
                return self.fopt(Node("App",[expr,e2]),rest)
        return (expr,toks)
    def items(self,toks):
        #if toks:
        t,ts = self.unpack(toks)
        if t not in [',',')']:
            e1,rest1 = self.expr(toks)
            return self.rest_item( [e1] ,rest1)
        elif t == ')':
            return ([],toks)
        elif t == ',' and self.unpack(ts)[0] == ')':
            return ([],ts)
        else:
            Expected(f"items {toks}")
    def rest_item(self,e1,toks):
        if toks:
            t,ts = self.unpack(toks)
            if t == ',':
                x,xs = self.unpack(ts)
                if x == ')': # drop t == drop ','
                    return (e1,ts)
                else:
                    e2,rest2 = self.expr(ts)
                    return self.rest_item( e1 + [e2],rest2)
            else:
                return (e1,toks)
        else:
            return (e1,toks)
keywords = ["if","then","else",
            "let","=","in",
            "fn",
            "=>",":",
            "[","]",
            "(",",",")","+","-","*","/"]
spectab = {
    "=":[">"],
}
separators = [" ","\n","\t"]
lex = Lex(spectab,keywords,separators)
parse = parser(keywords).read

class Env(type):
    def __new__(cls,name,parent,attrs):
        attrs["__name__"] = name
        if "__repr__" not in attrs.keys():
            attrs["__repr__"] = lambda self:self.__name__
        return type.__new__(cls,name,parent,attrs)
class Empty(metaclass=Env):
    pass
class Extend(metaclass=Env):
    def __init__(self,sym,val,env):
        self.sym = sym
        self.val = val
        self.env = env
    def __repr__(self):
        return f"[ {self.__name__} {self.sym} , {self.val} , {repr(self.env)} ]"
class enviroment(object):
    def __init__(self,init=Empty()):
        self.env = init
    def __repr__(self):
        return repr(self.env)
    def extend(self,sym,val):
        return enviroment( Extend(sym,val,self.env) )
    def apply(self,sym):
        # get sym
        temp = self.env
        while not isinstance(temp,Empty):
            if isinstance(temp,enviroment):
                temp = temp.env
            if isinstance(temp,Extend):
                ss,vv,temp = temp.sym,temp.val,temp.env
                if sym == ss:
                    return vv
        else:
            Expected(f"apply {sym} no bound variable in {self.env}")

def interpreter(ast,env):
    print( ast.name,ast.rest )
    if ast.name == "Var":
        val = env.apply(ast.rest[0])
        if val:
            return val
        else:
            Expected(f"not define {ast}")            
    elif ast.name == "Paren":
        return interpreter(ast.rest[0],env)
    elif ast.name == "Num":
        return ast.rest[0]
    elif ast.name == "Tuple":
        return tuple([interpreter(_ast,env) for _ast in ast.rest])
    elif ast.name == "Let":
        for k,v in ast.rest[0]:
            print("let:",k,v)
            if len(k) > 1 and v.name == "Tuple":
                for name,val in zip(k,v.rest):
                    env = env.extend(name,interpreter(val,env))
            else:
                env = env.extend(k[0],interpreter(v,env))
        print("let_env:",env) 
        return interpreter(ast.rest[1],env)
    elif ast.name == "If":
        cond,true,false = tuple(ast.rest)
        cond_val = interpreter(cond,env)
        if cond_val:
            return interpreter(true,env)
        return interpreter(false,env)
    elif ast.name == "Fn":
        return ast
    elif ast.name == "App":
        fun = interpreter(ast.rest[0],env)
        val = interpreter(ast.rest[1],env) # always retune a  tuple
        sym = fun.rest[0]
        body = fun.rest[1]
        print( "App:" ,sym,val )
        if len(sym) == len(val):
            for s,v in zip(sym,val):
                env = env.extend(s,v)
            print( "env:",env )
            return interpreter(body,env)
        else:
            Expected(f"function application args not equal {len(sym)} {len(val)}")
    elif ast.name in ["+","-","*","/"]:
        l,r = ast.rest[0],ast.rest[1]
        if ast.name == "+":
            return interpreter(l,env) + interpreter(r,env)
        elif ast.name == '-':
            return interpreter(l,env) - interpreter(r,env)
        elif ast.name == '*':
            return interpreter(l,env) * interpreter(r,env)
        elif ast.name == '/':
            return interpreter(l,env) / interpreter(r,env)
    else:
        Expected(f"not define {ast}")

__all__ = ["lex","parse","interpreter","Empty","Extend","enviroment"]
