#coding=utf-8
__doc__ = """
\033[0m 关闭所有属性
\033[1m 设置高亮度
\03[4m  下划线
\033[5m 闪烁
\033[7m 反显
\033[8m 消隐
\033[30m ~ \033[37m   前景色
\033[40m ~ \033[47m   背景色
--------------------
\033[nA 光标上移 n
\033[nB 光标下移 n
\033[nC 光标右移 n
\033[nD 光标左移 n
\033[y;xH 设置光标位置
\033[2J 清屏
\033[nK 若有 n 则从光标位置删除到行尾 ，若n为0则删除行
\033[s 保存光标位置
\033[u 恢复光标位置
\033[?25l 隐藏光标
\033[?25h 显示光标

\f FF 移动到下页开头 换页    012
\n LF 移动到下一行开头 换行  010
\r CR 当前位置移动到本行开头 013
\t HT 水平制表               009
ascii 和 转意符
"""
start = "\033["
end   = "\033[0m"
def move_up(n):
    return f"{start}{n}A"
def move_down(n):
    return f"{start}{n}B"
def move_left(n):
    return f"{start}{n}D"
def move_right(n):
    return f"{start}{n}C"
line_end = "\n\r\b"
line_start = "\r"
kill_line = f"{start}K"
clear = f"{start}2J"
def delete(n):
    return ('\b \b' * n )
light = 0
dark  = 1
back = {
    'black':40,
    'red'  :41,
    'green':42,
    'yellow':43,
    'blue'  :44,
    'purple' :45,
    'dark-green':46,
    'white':47,
    'add1':48,
    'add2':49 }
front = {
    'black':30,
    'red'  :31,
    'green':32,
    'yellow':33,
    'blue'  :34,
    'purple' :35,
    'dark-green':36,
    'white':37,
    'add1':38,
    'add2':39 
}
def green( s ):
    return f"{start}0;0;32m{s}{end}"
from msvcrt import getch
import sys
def write(s):
    sys.stdout.write(s)
def run():
    buff = [ ]
    write( clear )
    write("\tWeclome vshell v1.0 beta.")
    write(move_down(1))
    write("\r")
    while 1:
        sys.stdout.flush()
        c = getch()
        try:
            if 32 <= list(c)[0] <= 126:
                write( str(c,'utf-8') )
            #else:
            #    write( str(c,'utf-8') )
            #write( str(list(c)[0]) )
        except Exception as e:
            write( str(list(c)[0]) )
        if c == b'\r':
            break
        elif c == bytes([11]):
            # Ctrl + k
            write( kill_line )
        elif c == bytes([8]):
            # backspace
            write( delete(1) )
        elif c == bytes([6]):
            # Ctrl + f
            write( move_right(1) )
        elif c == bytes([1]):
            # Ctrl + a
            write( line_start )
        elif c == bytes([5]):
            # Ctrl + e
            write( line_end )
        elif c == bytes([2]):
            # Ctrl + b
            write( move_left(1) )
        elif c == bytes([14]):
            # Ctrl + n
            write( move_down(1) )
        elif c == bytes([16]):
            # Ctrl + p
            write( move_up(1) )
        elif c == bytes([224]):
            try:
                sym = str(getch(),'utf-8')
            except:
                sym = ''
            if sym == 'M':
                # -> right arrow
                write( move_right(1) )
            elif sym == 'K':
                # <- left arrow
                write( move_left(1) )
            elif sym == 'H':
                # /|\ up arrow
                #  |
                write( move_up(1) )
            elif sym == 'P':
                #  |  down arrow
                # \|/
                write( move_down(1) )

run()
