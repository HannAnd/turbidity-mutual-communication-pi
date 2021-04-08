#possibility: the sleep delay just means the Pi waits to read whatever the next
#value in line is rather than reading whatever is available /at that particular moment/

# test code for mutual communication between Pi and Arduino
# Pi should send command to Arduino to read and then send turbidity
# once Pi receives turbidity it will tell the Arduino to open
    # a specific relay channel based on the turbidity value

import serial    # allows Pi to read serial data
#import threading    # allows Pi to create threads (needed for timer)
import time    # allows Pi to keep track of time
wait = "no"    # to stop the Pi from spam printing "Read request sent"
start = "yes"    # for closing all relay channels at start up

if __name__ == '__main__':    #defines this file as primary module
    # calls the serial monitor using serial.Serial at port 'ttyACM0' (change if needed),
    # sets the baud rate (needs to be the same as the Arduino), and sets a
    # timeout so that if the Arduino stops sending info the Pi doesn't
    # get stuck in a loop
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    # waiting for buffer to clear
    ser.flush()
    # closing all channels for a clean start of code
    ser.write(b"off\n")
    print("Starting with all channels off")
    # giving Serial time to open
    time.sleep(0.1)
    
    while True:    # creates an infinite loop because this should always
                   # be the primary module
        # printing that the read request was sent
        if wait == "no":
            print("Read request sent")
            # ensures the string is only printed once per request
            wait = "yes"
        # waiting for buffer to clear again, not sure if this is necessary
        ser.flush()
        # telling the Arduino to send a turbidity reading
        # the "b" encodes the string as bytes for transmission through
        # Serial and the \n indicates the end of the line
        ser.write(b"turbidread\n")
        wait = "yes"
        
        if ser.in_waiting > 0:
            # readline() reads all bytes in a line from serial monitor
            # decode() converts the bytes from their raw form to their
              # intended string
            # rstrip() removes "trailing characters" and excess white space from
              # the beginning/end of a line
            turbidity = ser.readline().decode('utf-8').rstrip()
            # prints turbidity reading for visibility
            print(turbidity)
        # sends commands to the Arduino about which relay channel to open
          # based on what the turbidity is
        # here we're using three liquids (plain water, concentrated coffee,
          # unconcentrated coffee) and then the fourth channel is when the
          # sensor is just held in the air
            # below values have to be calibrated in a separate script
            if float(turbidity) <= 4.65 and float(turbidity) > 4.50:    # plain water
                ser.write(b"channel1\n")    # channel 1
                print("Plain water.")
                print("Move sensor now (10 sec)")
                # allows for a 10 second delay to move the sensor
                time.sleep(10)
                wait = "no"
            elif float(turbidity) <= 4.50 and float(turbidity) > 4.30:    # weak coffee
                ser.write(b"channel2\n")    # channel 2
                print("Weak coffee.")
                print("Move sensor now (10 sec)")
                # allows for a 10 second delay to move the sensor
                time.sleep(10)
                wait = "no"
            elif float(turbidity) <= 2.60 and float(turbidity) > 2.50:    # strong coffee
                ser.write(b"channel3\n")    # channel 3
                print("Strong coffee.")
                print("Move sensor now (10 sec)")
                # allows for a 10 second delay to move the sensor
                time.sleep(10)
                wait = "no"
            elif float(turbidity) <= 4.10 and float(turbidity) > 3.00:    # air detection
                ser.write(b"channel4\n")    # channel 4
                print("Air detected.")
                print("Move sensor now (10 sec)")
                # allows for a 10 second delay to move the sensor
                time.sleep(10)
                wait = "no"
            # should only happen if something has gone wrong
            else:
                ser.write(b"off\n")    # all channels off
                print("Invalid turbidity reading.")
                print("Move sensor now (10 sec)")
                # allows for a 10 second delay to move the sensor
                time.sleep(10)
                wait = "no"

#and then after this I would like to create an alternative method where it checks
#every set amount of time based on the Pi's internal clock
    #the first technique will be used for the Pi logging the turbidity of a
    #chamber after a water change (prolly 30 minute later)
    #the second technique will be used in automating when the water changes
    #themselves will happen