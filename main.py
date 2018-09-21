#coding=utf-8
from lang import *
import sys
def input (symbol) :
    result= ''
    sys.stdout.write('\r' + symbol)
    for line in sys.stdin:
        if line[0] is '\n':
            break
        result += line
    return result

def repl():
    env = {
        'a':2,
        'b':3,
    }
    try:
        while 1:
            stdin = input(">> ")
            inp = stdin.replace("\n","")
            if inp == ":q":
                print('repl exit.')
                break
            else:
                try:
                    inp = lex.Tokenise(stdin)
                    ast = parse(inp)
                    print("=>",ast)
                    val = interpreter(ast,env)
                    print("|>",val)
                except Exception as e:
                    print("||",e )
    except KeyboardInterrupt:
        print('\b\b\brepl exit.')
# need implement infix need first scan readline infix define add to enviroment and remove it line
if __name__ == "__main__":
    repl()
