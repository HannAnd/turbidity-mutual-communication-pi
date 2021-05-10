# for calibrating the turbidity readings in the mutual communication test code

import serial    # allows Pi to read serial data
#import threading    # allows Pi to create threads (needed for timer)
import time    # allows Pi to keep track of time
cycle = 4
counter = 1

if __name__ == '__main__':    #defines this file as primary module
    # calls the serial monitor using serial.Serial at port 'ttyACM0',
    # sets the baud rate (needs to be the same as the Arduino), and sets a
    # timeout so that if the Arduino stops sending info the Pi doesn't
    # get stuck in a loop
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    # clearing out the internal buffer of the file
    ser.flush()
    
    while True:    # creates an infinite loop because this should always
                   # be the primary module
        # telling the Arduino to send a turbidity reading
        # the "b" encodes the string as bytes for transmission through
        # Serial and the \n indicates the end of the line
        # delay between readings to prevent spamming
        time.sleep(5)
        # requests turbidity reading from Arduino
        ser.write(b"1\n")
         # readline() reads all bytes in a line from serial monitor
            # decode() converts the bytes from their raw form to their
            # intended string
            # rstrip() removes "trailing characters" and excess white space from
            # the beginning/end of a line
        if ser.in_waiting > 0:
            turbidity = ser.readline().decode('utf-8').rstrip()
            # check the printed value ranges to calibrate the main file
            print("Reading " + str(counter))
            print(turbidity)
            counter += 1
        # short delay between read command and channel command to avoid spamming
        time.sleep(0.5)
        # opens one of the relay channels to verify relay commands are working
        ser.write(str(cycle).encode('utf-8'))
        print(cycle)
        # cycles through a different relay command for each reading
        if cycle == 8:
            cycle = 4
        else:
            cycle += 1
        
            
        