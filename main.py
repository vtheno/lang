#coding=utf-8
from lang import *
from Parser import Node
from datatype import enviroment
from eval import interpreter
import sys
from pprint import pprint
env = enviroment()
#env = env.extend("~",interpreter(parse(lex.Tokenise("fn x => 0 - x")),env) )
#env = env.extend('abs',interpreter(parse(lex.Tokenise("fn i => if i then i else 0 - i")),env))
#parse(lex.Tokenise("infix ::"))
#env = env.extend('::',interpreter(parse(lex.Tokenise("fn (a,b) => (a,b)")),env) )
#env = env.extend('$',interpreter(parse(lex.Tokenise("fn a => (fn b => a b)")),env))
#parse(lex.Tokenise("infix 3 ."))
#env = env.extend('.',interpreter(parse(lex.Tokenise("fn (obj,method) => (method obj)")),env))
#env = env.extend('Y',interpreter(parse(lex.Tokenise("""
#fn f =>
#let 
#    self = fn x => (fn n => (f (x x)) n)
#in  fn n => (f (self self)) n
#""")),env))

print( "init_env:",end='')
pprint(  env )
pprint( p.infix_tab )
def input (symbol) :
    result= ''
    sys.stdout.write('\r' + symbol)
    for line in sys.stdin:
        if line[0] is '\n':
            break
        result += line
    return result
def repl():
    global env
    try:
        while 1:
            stdin = input(">> ")
            inp = stdin.replace("\n","")
            if inp == ":q":
                print('\nrepl exit.')
                break
            elif inp == ":e":
                pprint(env)
            else:
                #try:
                inp = lex.Tokenise(stdin)
                ast = parse(inp)
                val = interpreter(ast,env)
                print("|>",val)
                print("\r=> ",end='')
                pprint(dict(ast._asdict()))
                #except Exception as e:
                #    print("||",e )
    except KeyboardInterrupt:
        print('\b\b\b\nrepl exit.')
# need implement infix need first scan readline infix define add to enviroment and remove it line
# profound
if __name__ == "__main__":
    if len(sys.argv) > 1:
        argv = sys.argv[1:]
        filename = argv[0]
        with open(filename,'r') as File:
            stdin = File.read()
            try:
                inp = lex.Tokenise(stdin)
                ast = parse(inp)
                val = interpreter(ast,env)
                print("|>",val)
                print("=>",end='')
                pprint(dict(ast._asdict()))
            except Exception as e:
                print("||",e )
    else:
        repl()
