#!/usr/bin/python
# sockServer.py
# W Parker Mackenzie 2018
#
# Repo : https://github.com/wparkermackenzie/examples
# License : The Unlicense
#
#
#
# A simple example of opening and then listening on multiple ports
#

import argparse
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
        print( "Closing %s:%d" % s.getsockname())
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
parser.add_argument('start',        type=int, help='First port number to bind to')
parser.add_argument('number',       type=int, help='Number of ports to open')
parser.add_argument('timeout',      type=int, help='Duration in seconds to leave sockets open')
parser.add_argument('--interface',            help='IP address asscociated with the interface', default='')
arguments=parser.parse_args()
st=arguments.start
nu=arguments.number
to=arguments.timeout
h=arguments.interface

print( "Opening stream sockets on port numbers %d to %d waiting %d seconds" % (st,st+nu-1,to))

l = []

#
# Register a signal handler to shutdown the application in a well defined manner
#
signal.signal(signal.SIGINT, sighandler)


#
# Open and bind to the port numbers
#
for i in range(0,nu):
    p = st + i
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(0)
        s.bind((h,p))
        s.listen(1)
        l.append(s)
        print( 'Listening on %s:%d' % s.getsockname())
    except socket.error:
        print( 'FAILED to open port %d' % (p))

#
# Wait for the port numbers to do something interesting
#
while 1:
    r,w,e = select.select( l,l,l, to )
    for s in r:
        me=s.getsockname()
        connection,addr=s.accept()
        rxbuf=connection.recv(4096)
        bs= ":".join("{:02x}".format(ord(c)) for c in rxbuf)
        print('RX [%s:%d->%s:%d] %s' % (addr[0],addr[1],me[0],me[1],bs))
        #print('RX %s' % bs)


#
# Before exiting the application close existing connections
#
terminate()




