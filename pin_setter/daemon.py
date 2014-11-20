#!/usr/bin/env python
# see http://stackoverflow.com/questions/11597284/how-do-i-create-a-python-socket-server-that-listens-on-a-file-descriptor
import socket
import os, os.path
import time

sockfile = "/tmp/communicate.sock"

if os.path.exists( sockfile ):
  os.remove( sockfile )

print "Opening socket..."

server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
server.bind(sockfile)
os.chmod(sockfile, 0777)  # allow anyone to read/write
server.listen(5)

print "Listening..."
while True:
  conn, addr = server.accept()

  print 'accepted connection'

  while True:

    data = conn.recv( 1024 )
    if not data:
        break
    else:
        print "-" * 20
        print data
        if "DONE" == data:
            break
print "-" * 20
print "Shutting down..."

server.close()
os.remove( sockfile )

print "Done"