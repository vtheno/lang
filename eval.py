#coding=utf-8
from datatype import *
from lang import p
from Parser import Node
def interpreter(ast,env):
    #print( ast.name,ast.rest )
    # can rewrite using state machine
    if ast.name == "Var":
        #print( "var:",ast.name,ast.rest[0],env )
        return env.apply(ast.rest[0])
    elif ast.name == "Paren":
        #print("paren_env:",env)
        return interpreter(ast.rest[0],env)
    elif ast.name == "Num":
        return ast.rest[0]
    elif ast.name == "Tuple":
        return Tuple([interpreter(_ast,env) for _ast in ast.rest])
    elif ast.name == "Let":
        print( ast )
        for k,v in ast.rest[0]:
            print( "let:",k,v )
            #val = interpreter(v,env) 
            #val = val.val if isinstance(val,Tuple) else [val]
            #len_k = len(k)
            #if len_k == 1 and isinstance(val,tuple) and len(val) != 1:
            #    val = [val]
            #len_v = len(val)
            #if len_k == len_v:
            #    for n,v in zip(k,val):
            #        env = env.extend(n,v)
            #        if isinstance(v,Proc):
            #            #print( "v:",v.env )
            #            v.env = v.env.extend(n,v)
            #            # update the function name binding to enviroment
            #            # next update enviroment to the function env
            #            #print( "v:",v.env )
            #elif len_k < len_v:
            #    Expected(f"value unpack to variable to greate ( have {len_v} value to {len_k} variable")
            #elif len_k > len_v and len_v > 0:
            #    Expected(f"value unpack to variable to less ( have {len_v} value to {len_k} variable {ast}")
            #else:
            #    Expected(f"value can't unpack to variable")
        print("let_env:",env) 
        return interpreter(ast.rest[1],env)
    elif ast.name == "App":
        fun = interpreter(ast.rest[0],env)
        val = interpreter(ast.rest[1],env)
        #print( "apply:",fun,val )
        if isinstance(fun,Proc):
            val = val.val if isinstance(val,Tuple) else [val]
            sym,body,env = fun.var,fun.body,fun.env
            len_s = len(sym)
            if len_s == 1 and isinstance(val,tuple) and len(val) != 1:
                val = [val]
            len_v = len(val)
            if len_s == len_v:
                for s,v in zip(sym,val):
                    env = env.extend(s,v)
                print( "app_env:",env )
                return interpreter(body,env)
            else:
                Expected(f"function application args not equal {len_s} {len_v}")
        else:
            Expected(f"value {val} can't apply {fun}")
    elif ast.name == "If":
        cond,true,false = tuple(ast.rest)
        cond_val = interpreter(cond,env)
        if cond_val:
            return interpreter(true,env)
        return interpreter(false,env)
    elif ast.name == "Fn":
        var,body = ast.rest[0],ast.rest[1]
        #print( "Fn:",var,env)
        return Proc(var,body,env)
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
    elif ast.name in p.user_infix:
        fun = Node("Var",[ast.name])
        arg = Node("Tuple",ast.rest)
        #print( fun,arg )
        return interpreter( Node("App",[fun,arg]),env)
    elif ast.name == 'Infix':
        level,assoc,symop = tuple(ast.rest)
        return Node("Var",[symop])
    elif ast.name == 'Infixr':
        level,assoc,symop = tuple(ast.rest)
        return Node("Var",[symop])
    else:
        Expected(f"not implement {ast}")

__all__ = ["interpreter"]
