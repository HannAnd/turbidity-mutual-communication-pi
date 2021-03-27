# for calibrating the turbidity readings inthe mutual communication test code

import serial    # allows Pi to read serial data
#import threading    # allows Pi to create threads (needed for timer)
import time    # allows Pi to keep track of time
wait = "no"

if __name__ == '__main__':    #defines this file as primary module
    # calls the serial monitor using serial.Serial at port 'ttyACM0',
    # sets the baud rate (needs to be the same as the Arduino), and sets a
    # timeout so that if the Arduino stops sending info the Pi doesn't
    # get stuck in a loop
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
        # clearing out the internal buffer of the file
    # kind of like clearing the workspace in R
    # basically keeps the variable clean so it doesn't return old values
    ser.flush()
    
    while True:    # creates an infinite loop because this should always
                   # be the primary module
        # telling the Arduino to send a turbidity reading
        # the "b" encodes the string as bytes for transmission through
        # Serial and the \n indicates the end of the line
        if wait == "no":
            ser.write(b"turbidread\n")
            wait = "yes"
        elif wait == "yes":
            time.sleep(5)
            ser.write(b"turbidread\n")
        # readline() reads all bytes in a line from serial monitor
            # decode() converts the bytes from their raw form to their
            # intended string
            # rstrip() removes "trailing characters" and excess white space from
            # the beginning/end of a line
        if ser.in_waiting > 0:
            turbidity = ser.readline().decode('utf-8').rstrip()
            # just printing for visibility
            print(turbidity)