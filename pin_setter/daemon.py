#!/usr/bin/env python -u
# see http://stackoverflow.com/questions/11597284/how-do-i-create-a-python-socket-server-that-listens-on-a-file-descriptor
import socket
import os, os.path
import time
import sys
import RPi.GPIO as GPIO

# GPIO pin set up.
GPIO.setmode(GPIO.BOARD)
NITE = 5
LITE = 3
GPIO.setup(NITE, GPIO.OUT)
GPIO.setup(LITE, GPIO.OUT)

STATES = {    # nite, lite
  "nite":     [1,     0],
  "lite":     [0,     1],
  "off":      [0,     0],
}

# Start up with both nite and lite on
GPIO.output(NITE, 1)
GPIO.output(LITE, 1)

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
        #sys.stdout.write("-" * 20 + "\n")
        sys.stdout.write(data + "\n")
        if data in STATES.keys():
          GPIO.output(NITE, STATES[data][0])
          GPIO.output(LITE, STATES[data][1])

          # Send the newly-setup state back to the socket
          conn.send(data)
          
        if "DONE" == data:
            break
sys.stdout.write("-" * 20 + "\n")
sys.stdout.write("Shutting down..." + "\n")

server.close()
os.remove( sockfile )
GPIO.cleanup()

sys.stdout.write("Done" + "\n")