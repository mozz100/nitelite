#!/usr/bin/env python -u
# -u means unbuffered output.
# Lots of this code just lifted from
# http://stackoverflow.com/questions/11597284/how-do-i-create-a-python-socket-server-that-listens-on-a-file-descriptor

import socket, os, time, sys
import RPi.GPIO as GPIO

# GPIO pin set up, board mode for pin numbers.
# Most convenient to use pin 6 for 0V/ground.
NITE = 5
LITE = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(NITE, GPIO.OUT)
GPIO.setup(LITE, GPIO.OUT)

nite_pwm = GPIO.PWM(NITE, 100)  # PWM at 100Hz

STATES = {    # nite, lite
  "bed":      [100,   0],
  "lite":     [0,     1],
  "nite":     [10,    0],
  "off":      [0,     0],
}

def set_pins(new_state, conn):
  global nite_pwm

  # Set the pins
  nite_pwm.start(NITE, STATES[new_state][0])  # PWM on the NITE pin
  GPIO.output(LITE, STATES[new_state][1])
  
  # Send (echo) the newly-setup state back to the calling process,
  # so the UI gets a notification that we're done
  conn.send(data)

ACTIONS = {
  "nite": set_pins,
  "lite": set_pins,
  "off":  set_pins,
  "bed":  set_pins,
}

# Start up with both nite and lite on.
nite_pwm.start(NITE, 100)
GPIO.output(LITE, 1)

sockfile = "/var/nitelite/communicate.sock"

# Delete socket file if it exists
if os.path.exists( sockfile ):
  os.remove( sockfile )

sys.stdout.write("Opening socket..." + "\n")

# Create socket file with 777 permissions
server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
server.bind(sockfile)
os.chmod(sockfile, 0777)  # allow anyone to read/write
server.listen(5)

sys.stdout.write("Listening..." + "\n")
while True:
  conn, addr = server.accept()

  sys.stdout.write('Accepted connection.' + "\n")

  while True:

    data = conn.recv( 1024 )
    if not data:
        break
    else:
        sys.stdout.write(data + "\n")

        # React to commands like "nite", or "lite"
        if data in ACTIONS.keys():
          # Call the function defined in ACTIONS, passing
          # data and conn as parameters
          ACTIONS[data](data, conn)
          
        if "DONE" == data:
            break

sys.stdout.write("-" * 20 + "\n")
sys.stdout.write("Shutting down..." + "\n")

server.close()
os.remove( sockfile )
GPIO.cleanup()

sys.stdout.write("Done" + "\n")