#coding=utf-8
from shell import *
import re
from subprocess import Popen,PIPE
from filesystem import * 
import os
def select(s):
    return f"{start}0;0;{front['green']}m{s}{end}"
def fuzzy(items):
    def warp(inp):
        out =  [ ]
        pattern = ".*?".join(inp)
        regex = re.compile(pattern)
        for item in items:
            match = regex.search(item)
            if match:
                out += [(len(match.group()), match.start(), item)]
        return [x for _, _, x in sorted(out)]
    return warp
fs = FileSystem('test')
fs.load()
def listdir():
    items = fs.ls()
    outs = [ ]
    for i in items:
        if i["type"] == "dir":
            outs += [ f"{start}0;1;{front['blue']}m{i['name']}{end}" ]
        elif i["type"] == "file":
            outs += [ f"{start}0;1;{front['green']}m{i['name']}{end}" ]
    return outs
def excute(cmd,args):
    if cmd == "pwd":
        out = fs.getcwd()
        write( out )
        write( new_line )
        return 
    elif cmd == "cd":
        path = args[0]
        out = fs.change_dir(path)
        write( out )
        write( new_line )
        return 
    elif cmd == "clear":
        write( clear )
        write( new_line )
        return 
    elif cmd == "ls":
        outs = listdir()
        write( '  '.join(outs) )
        write( new_line )
        return 
    elif cmd == "whoami":
        write( "root" )
        write( new_line )
        return
    elif cmd == "mkdir":
        name = args[0]
        out = fs.mkdir(name)
        write( out )
        write( new_line )
    elif cmd == "rmdir":
        name = args[0]
        out = fs.rmdir(name)
        write( out )
        write( new_line )
    elif cmd == "touch":
        name = args[0]
        out = fs.touch(name)
        write( out )
        write( new_line )
    elif cmd == "remove":
        name = args[0]
        out = fs.remove(name)
        write( out )
        write( new_line )
    else:
        write( "Command Not Found!" )
        write( new_line )
        return
fz = fuzzy(
    [ "pwd",
      "cd",
      "clear",
      "ls",
      "mkdir",
      "rmdir",
      "touch",
      "remove",
      "whoami",
 ])
def input(syms=''):
    #write( clear )
    #write( "\t\tWeclome vshell v1.0 beta \n" )
    buff = [ ]
    write("\r")
    write(syms)
    #index = 0
    while 1:
        sys.stdout.flush()
        c = getwch()
        code = ord(c)
        #write( move_up(1) )
        #write( str(code) )
        #write( move_left(len(str(code))) )
        #write( move_down(1) )
        if 32 <= code <= 126 or  0x4E00 <= code <= 0x9FA5:
            buff.append ( c )
            #write( c )
        elif code == 13:
            break
        elif code == 8:
            # backspace
            if buff:
                buff.pop()
                write( delete(1) )
        elif code == 9:
            # tab
            inp = ''.join(buff).split(' ')
            items = fz(inp[-1])
            index = 0
            if items:
                write( "\n\r" )
                for i in range(len(items)):
                    if index == i:
                        write( select(items[i]) )
                        write( new_line )
                    else:
                        write( items[i] )
                        write( new_line )
            while items:
                t = ord(getwch())
                if t == 9:
                    if index == len(items) - 1:
                        index = 0
                    else:
                        index += 1
                    sys.stdout.flush()
                    write( move_up(len(items) ) ) # move up n and move to start
                    write( line_start )
                    for i in range(len(items)):
                        if index == i:
                            write( select(items[i]) )
                            write( new_line )
                        else:
                            write( items[i] )
                            write( new_line )
                elif t == 13:
                    if len(inp) == 1:
                        buff = [i for i in items[index]]
                    else:
                        inp.pop()
                        inp += [items[index]]
                        buff = list(' '.join(inp))
                    break
                elif t == 224:
                    t1 = ord(getwch())
                    break
                else:
                    break
            if items:
                for i in items:
                    write(move_up(1))
                    write(line_start)
                    write(kill_line)
                write(move_up(1))
                write(line_start)
                write(kill_line)
        elif code == 2:
            # ctrl + b
            # write( move_left( 1 ) )
            pass
        elif code == 6:
            # ctrl + f
            # write( move_right(1) )
            pass
        elif code == 11:
            # ctrl + k
            # write( kill_line )
            pass
        elif code == 1:
            # ctrl + a
            # write( line_start )
            pass
        elif code == 5:
            # ctrl + e
            # write( line_end )
            pass
        elif code == 14:
            # ctrl + n
            # write( move_down(1) )
            pass
        elif code == 16:
            # ctrl + p
            # write( move_up(1) )
            pass
        elif code == 224:
            c1 = getwch()
            #if c1 == 'P':
            #    write( move_down(1) )
            #elif c1 == 'H':
            #    write( move_up(1) )
            #elif c1 == 'M':
            #    write( move_right(1) )
            #elif c1 == 'K':
            #    write( move_left(1) )
        write( f"\r{syms}{''.join(buff)}" )
    write( new_line )
    return ''.join(buff)

def repl():
    write( clear )
    write( "\t\tWeclome vshell v1.0 beta \n" )
    while 1:
        out = input(">> ")
        if out == ":q":
            break
        outs = out.split(' ')
        cmd,args = outs[0],outs[1:]
        try:
            excute(cmd,args)
        except FileSystemError as e:
            write( str(e) )
            write( new_line )
repl()
