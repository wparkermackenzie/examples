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

# To do: 
# - Resolve addresses to names and process ids
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
parser.add_argument('--timeout',    type=int, help='Timeout (seconds) waiting on inactive sockets'          ,default=10)
parser.add_argument('--interface',            help='IP address asscociated with the interface'              ,default='')
arguments=parser.parse_args()
st=arguments.start
nu=arguments.number if(arguments.number>0) else 1
to=arguments.timeout
h=arguments.interface
stp=st+nu-1 if( nu > 0 ) else st+nu
print( "Opening stream sockets on port numbers %d to %d" % (st,stp))

l = []

#
# Register a signal handler to shutdown the application in a well defined manner
#
signal.signal(signal.SIGINT, sighandler)


#
# Open and bind to the port numbers
#
for p in range(st,stp+1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(0)
        s.bind((h,p))
        s.listen(1)
        l.append(s)
        print( 'Listening on %s:%d' % s.getsockname())
    except socket.error:
        print( 'FAILED to open port %d' % (p))

if( 0 == len(l) ) :
    print( 'No open sockets' )
    terminate()
    sys.exit(0)
#
# Wait for the port numbers to do something interesting
#
while 1:
    r,w,e = select.select( l,l,l, to )
    for s in r:
        me=s.getsockname()
        try:
            connection,addr=s.accept()
            rxbuf=connection.recv(4096)
            bs= ":".join("{:02x}".format(ord(c)) for c in rxbuf)
            print('RX [%s:%d->%s:%d] %s' % (addr[0],addr[1],me[0],me[1],bs))
        except:
            print('RX [%s:%d->%s:%d] Nothing to receive' % (addr[0],addr[1],me[0],me[1]))


#
# Before exiting the application close existing connections
#
terminate()




