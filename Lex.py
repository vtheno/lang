#coding=utf-8
# add lex support float number
class Ident(object):
    def __init__(self,sym):
        self.sym = sym
    def __repr__(self):
        return f"id{ {self.sym} }"
class GetNextTokenErr(Exception) : pass
class Lex(object):
    def __init__(self,spectab,keywords,separators):
        self.spectab = spectab   # spectab : {str:[str]}
        self.keywords = keywords # keywords : [str]
        self.separators = separators
    def IsDigit(self,x : str ) -> bool :
        return '0' <= x <= '9'
    def IsLetter(self,x : str ) -> bool :
        return "a" <= x <= "z" or "A" <= x <= "Z"
    def IsLetterOrDigit(self,x : str) -> bool:
        return ("a" <= x <= "z" or "A" <= x <= "Z") or "0" <= x <= "9"
    def IsSeparator(self,x : str) -> bool :
        return x in self.separators#x == " " or x == "\n" or x == "\t" 
    def getTail(self,p,tok,lst):
        temp = lst
        while temp:
            x,temp = temp[0],temp[1:]
            if p(x):
                tok += x
            else:
                temp = [x] + temp
                self.inp = temp
                return tok
        else:
            self.inp = temp
            return tok
    def getSymbol(self,tok,lst):
        temp = lst
        while temp:
            x,temp = temp[0],temp[1:]
            #print( x,self.spectab.get(tok,[]) )
            if x in self.spectab.get(tok,[]):
                tok += x
            else:
                self.inp = [x] + temp
                return tok
        else:
            self.inp = [ ]
            return tok
    def Tokenise(self,inp):
        self.inp = list(inp)
        result = [ ]
        while self.inp:
            _x,l1 = self.inp[0],self.inp[1:]
            l = [_x] + l1
            if self.IsSeparator(_x):
                self.inp = l1
            else:
                if self.inp == []:
                    raise GetNextTokenErr("{} length < 1 !".format(self.inp))
                elif len(self.inp) == 1:
                    t,self.inp = self.inp[0],self.inp[1:]
                else:
                    x,xs = self.inp[0],self.inp[1:]
                    c,cs = xs[0],xs[1:]
                    if "a" <= x <= "z" or "A" <= x <= "Z":#self.IsLetter(x):
                        buf = f'{x}'
                        t = self.getTail(self.IsLetterOrDigit,buf,xs)
                    elif '0' <= x <= '9':#self.IsDigit(x):
                        buf = f'{x}'
                        t = self.getTail(self.IsDigit,buf,xs)
                    else:
                        if c in self.spectab.get(x,[]):
                            # symbol
                            t = self.getSymbol(''.join([x,c]),cs)
                        else:
                            t,self.inp = x,xs
                result = result + [t]
        return result#[r if r in self.keywords else Ident(r) for r in result]
"""
SpecTab = {
    "-":[">"],
    ":":[":"],
}
keywords = ["+","-","*","/","->","::"]
separators = ["\n","/"]
lex = Lex(SpecTab,keywords,separators)
inp = /index.jpg
print( lex.Tokenise(inp) )
print( {Ident('c'):233} )
"""
__all__ = ["Lex","GetNextTokenErr"]
