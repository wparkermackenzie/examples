#!/usr/bin/python
# sockServer.py
# W Parker Mackenzie 2018
#
#
#
# A simple example of opening and then listening on multiple ports
#

import argparse
import select
import socket
import time

#
# Parse command line arguments
#
parser = argparse.ArgumentParser(description='Open a stream socket on multiple ports')
parser.add_argument('start',    type=int, help='First port number to bind to')
parser.add_argument('number',   type=int, help='Number of ports to open')
parser.add_argument('timeout',  type=int, help='Duration in seconds to leave sockets open')
arguments=parser.parse_args()
st=arguments.start
nu=arguments.number
to=arguments.timeout

print( "Opening stream sockets on port numbers %d to %d waiting %d seconds" % (st,st+nu-1,to))

l = []

#
# Open and bind to the port numbers
#
for i in range(0,nu):
    h = ''
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
r,w,e = select.select( l,l,l, to )

#
# Close the port numbers
#
for s in l:
    print( "Closing %s:%d" % s.getsockname())
    s.close()





