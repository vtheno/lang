#coding=utf-8
from Parser import Expected
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
        return f"[ '{self.sym}':{self.val} , {repr(self.env)} ]"
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

class Proc(object):
    def __init__(self,var,body,env):
        self.var = var
        self.body = body
        self.env = env
    def __repr__(self):
        return f"fn({', '.join([i for i in self.var])})"
class Tuple(object):
    def __init__(self,val):
        self.val = tuple(val)
    def __repr__(self):
        if self.val:
            return f"({', '.join([repr(i) for i in self.val])})"
        return "()"
__all__ = ["Tuple","Proc","enviroment","Expected"]
