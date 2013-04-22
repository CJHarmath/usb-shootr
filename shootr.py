import sys
import platform
import time
import socket
import re
import json
import urllib2
import base64

import usb.core
import usb.util

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICE = None
DEVICE_TYPE = None

move_duration = 30
led_state = 0

try:
	# Python2
	import Tkinter as tk
except ImportError:
# Python3
	import tkinter as tk

root = tk.Tk()

def key(event):
	global move_duration, led_state	
	"""shows key or tk code for the key"""
	if event.keysym == 'Escape':
		root.destroy()
	#if event.char == event.keysym:
		# normal number and letter characters
		# print( 'Normal Key %r' % event.char )
	elif len(event.char) == 1:
		# charcters like []/.,><#$ also Return and ctrl/key
		# print( 'Punctuation Key %r (%r)' % (event.keysym, event.char) )
		if event.keysym == 'KP_Add':
			if move_duration < 35:
                        	move_duration = move_duration + 1
				print "move speed: %r" % (move_duration)
		if event.keysym == 'KP_Subtract':
		        if move_duration >= 6:
			        move_duration = move_duration -1
			        print "move speed %r" % (move_duration)
		if event.keysym == 'space':
			#send_cmd(FIRE)
			run_command('fire',1)
		if event.keysym == 'Return':
			if led_state == 0:			
				led(1)
				led_state=1
			else:
				led(0)
				led_state=0
		if event.keysym == 'BackSpace':
			led(0)
	else:
		# f1 to f12, shift keys, caps lock, Home, End, Delete ...
		#print( 'Special Key %r' % event.keysym )
		if event.keysym == 'Up':
			send_move(UP, move_duration)
			#time.sleep(0.5)
		if event.keysym == 'Down':
			send_move(DOWN, move_duration)
			#time.sleep(0.5)
		if event.keysym == 'Right':
			send_move(RIGHT, move_duration)
			#time.sleep(0.5)
		if event.keysym == 'Left':
			send_move(LEFT, move_duration)
			#time.sleep(0.5)

def send_cmd(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])

def led(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        print("There is no LED on this device")

def send_move(cmd, duration_ms):
    led(1)
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)
    led(0)


def run_command(command, value):
    command = command.lower()
    if command == "right":
        send_move(RIGHT, value)
    elif command == "left":
        send_move(LEFT, value)
    elif command == "up":
        send_move(UP, value)
    elif command == "down":
        send_move(DOWN, value)
    elif command == "zero" or command == "park" or command == "reset":
        # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "led":
        if value == 0:
            led(0)
        else:
            led(1)
    elif command == "fire" or command == "shoot":
	#led(1)
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to the shot, then allow for reload time after.
        for i in range(value):
            send_cmd(FIRE)
	    print 'fired!'
            time.sleep(4)
            #print 'sleeped 4'
            send_cmd(FIRE)
	    #print 'fired 2'
	    time.sleep(0.2)
            send_move(LEFT, 5)
            #time.sleep(4)
            #led(0)
    else:
        print "Error: Unknown command: '%s'" % command


def run_command_set(commands):
    for cmd, value in commands:
        run_command(cmd, value)

def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    # and original USB Launcher
    global DEVICE 
    global DEVICE_TYPE

    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
        if DEVICE is None:
            raise ValueError('Missile device not found')
        else:
            DEVICE_TYPE = "Original"
    else:
        DEVICE_TYPE = "Thunder"

    

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered    

    DEVICE.set_configuration()
def keyPress(event, tk):
    ch = event.char
    if ch == '\\':
        tk.destroy()
    else:
        print ch


def main(args):
	setup_usb()
	print move_duration	
	print( "Press a left, right, up, down, +, -, space (Escape key to exit):" )
	root.bind_all('<Key>', key)
	# don't show the tk window
	#root.withdraw()
	root.mainloop()

if __name__ == '__main__':
    main(sys.argv)
