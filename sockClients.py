#!/usr/bin/python
# sockClients.py
# W Parker Mackenzie 2018
#
# Repo : https://github.com/wparkermackenzie/examples
# License : The Unlicense
#
# A simple example of a client sending to server with multiple ports
#


import argparse
import random
import re
import select
import signal
import socket
import sys
import time

l=[]

#
# Function to close existing connections
#
def terminate():
    for s in l:
        print( "CLOSE     [%s:%d]" % s.getsockname())
        s.close()

#
# Function to handle SIGINT in a well defined manner
#
def sighandler(sig,frame):
    terminate()
    sys.exit(0)


#
# Parse command line arguments
#
parser = argparse.ArgumentParser(description='Open a stream socket on multiple ports')
parser.add_argument('server'                    ,help='Address of the server'                                  ,default='127.0.0.1')
parser.add_argument('start'        ,type=int    ,help='First port number to send to')
parser.add_argument('number'       ,type=int    ,help='Number of ports to send on')
parser.add_argument('--fill'       ,type=int    ,help='Number of bytes of pseudo random data to append'        ,default=0)
parser.add_argument('--zfill'      ,type=int    ,help='Number of bytes of zero data to append'                 ,default=0)
parser.add_argument('--payload'                 ,help='List of bytes to send in hexadecimal format'            ,default='48:45:4c:4c:4f')
parser.add_argument('--period'     ,type=float  ,help='Number of seconds between sending packets'              ,default=15)
arguments=parser.parse_args()
st=arguments.start
nu=arguments.number if(arguments.number>0) else 1
wt=arguments.period
h=arguments.server
pay=arguments.payload
rfill=arguments.fill
zfill=arguments.zfill
stp=st+nu-1 if( nu > 0 ) else st+nu
print( "Attaching to server %s on port numbers %d to %d" % (h,st,stp))

l = []

#
# Register a signal handler to shutdown the application in a well defined manner
#
signal.signal(signal.SIGINT, sighandler)

#
# Process the payload
#
paylist=re.split('\W+',pay)
dta=''
for c in paylist:
    dta = dta + chr(int(c,16))

#
# Connect to the ports
#

def connect(addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        l.append(s)
        print( 'CONNECT   [%s:%d->%s:%d] SUCCEEDED' % (s.getsockname()[0],s.getsockname()[1],s.getpeername()[0],s.getpeername()[1]))
    except socket.error:
        print( 'CONNECT   [->%s:%d] FAILED' % (addr[0],addr[1]))

def reconnect():
    for p in range(st,stp+1):
        addr=(h,p)
        connect(addr)

while 1:
    if( 0 == len(l) ):
        reconnect()
    else:
        for s in l:
            try:
                addr=s.getpeername()
                me=s.getsockname()
                fill=''
                for i in range(0,rfill):
                    fill = fill + chr(random.randint(0,255))
                fillz=''
                for i in range(0,zfill):
                    fillz = fillz + chr(0)
                txbuf=dta + fill + fillz
                s.sendall(txbuf)
                bs= ":".join("{:02x}".format(ord(c)) for c in txbuf)
                print('TRANSMIT  [%s:%d->%s:%d] %s' % (me[0],me[1],addr[0],addr[1],bs))
            except socket.error:
                print('TRANSMIT  [%s:%d->%s:%d] Failed' % (me[0],me[1],addr[0],addr[1]))
                try:
                    l.remove(s)
                    s.close()
                    connect(addr)
                except socket.error:
                    pass

    time.sleep(wt)

#
# Before exiting the application close existing connections
#
terminate()




