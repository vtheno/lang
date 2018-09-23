#coding=utf-8
from colorshow import *
from msvcrt import getch
import sys
def color( buff ):
    buff = ''.join(buff)
    return show( buff )
def input( sym ):
    buff = [ ]
    sys.stdout.write( f"\r{sym}")
    sys.stdout.flush()
    while 1:
        c = getch()
        if c == b'\xe0':
            c = getch()
            #print( c )
            if c == b'S':
                temp = '\x08'
            elif c == b'M':
                pass
            elif c == b'K':
                pass
            elif c == b'H':
                pass
            elif c == b'P':
                tmp = (''.join(buff)).split(' ')
                results = fuzzy(tmp[-1])
                index = 0
                if results:
                    print ()
                    for i in range(len(results)):
                        if index == i:
                            print( select(results[i]) )
                        else:
                            print( results[i] )
                while results:
                    t = getch()
                    if t == b'\xe0':
                        t = getch()
                        if t == b'P':
                            if index == len(results) - 1:
                                index = 0
                            else:
                                index += 1
                            sys.stdout.flush()
                            sys.stdout.write(f"\033[{len(results)}A\r")
                            for i in range(len(results)):
                                if index == i:
                                    print( select(results[i]) )
                                else:
                                    print( results[i] )
                        elif t == b'H':
                            if index == 0:
                                index = len(results) -1
                            else:
                                index -= 1
                            sys.stdout.flush()
                            sys.stdout.write(f"\033[{len(results)}A\r")
                            for i in range(len(results)):
                                if index == i:
                                    print( select(results[i]) )
                                else:
                                    print( results[i] )
                    elif t == b'\r':
                        if len(tmp) == 1:
                            buff = [i for i in results[index]]
                        else:
                            tmp.pop()
                            tmp += [results[index]]
                            buff = list(' '.join(tmp))
                        break
                if results:
                    for i in results:
                        sys.stdout.write(f"\033[1A\r")
                        sys.stdout.write(f"\033[0K")
                    sys.stdout.write(f"\033[1A\r")
                    sys.stdout.write(f"\033[0K")
                    #sys.stdout.write(f"\033[2J") #clear
                    #sys.stdout.write(f"\033[K") # clear current line
            temp = ''
        else:
            temp = str(c,'utf8')
        if temp == "\r" or temp == "\n":
            break
        elif temp == '\x08':
            sys.stdout.write( f"\b" + " ")
            if buff:
                buff.pop()
        elif temp:
            buff += [temp]
            #print( temp )
        sys.stdout.write( f"\r{sym}{color(buff)}" )
        sys.stdout.flush()
    sys.stdout.write("\n")
    return ''.join(buff)
print( "\nout:",input(">> ") )
