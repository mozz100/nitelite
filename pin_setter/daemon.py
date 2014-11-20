#!/usr/bin/env python -u
# see http://stackoverflow.com/questions/11597284/how-do-i-create-a-python-socket-server-that-listens-on-a-file-descriptor
import socket
import os, os.path
import time
import sys

sockfile = "/tmp/communicate.sock"

if os.path.exists( sockfile ):
  os.remove( sockfile )

sys.stdout.write("Opening socket..." + "\n")

server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
server.bind(sockfile)
os.chmod(sockfile, 0777)  # allow anyone to read/write
server.listen(5)

sys.stdout.write("Listening..." + "\n")
while True:
  conn, addr = server.accept()

  sys.stdout.write('accepted connection' + "\n")

  while True:

    data = conn.recv( 1024 )
    if not data:
        break
    else:
        sys.stdout.write("-" * 20 + "\n")
        sys.stdout.write(data + "\n")
        if "DONE" == data:
            break
sys.stdout.write("-" * 20 + "\n")
sys.stdout.write("Shutting down..." + "\n")

server.close()
os.remove( sockfile )

sys.stdout.write("Done" + "\n")