#################################
# GPS file
# This file should control the GPS.
# Tips found here: http://ozzmaker.com/using-python-with-a-gps-receiver-on-a-raspberry-pi/#comments
# Author: Arysson Oliveira
#################################

import serial
import pynmea2

#serial port to connect with GPS board
port = "/dev/serial0"

class GPS():
    def __init__(self):
        self.TimeZone = -3
        #main infos returned from GPS board
        self.Timestamp = "0"
        self.Lat = "0"
        self.Lon = "0"
        self.Altitude = "0"
        self.Satellites = "0"
        self.Timestamp = "0"

        global serialPort
        #Initializing a serial connection
        serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)

    def updatePosition(self):
        #Read a line returned from the GPS
        readline = serialPort.readline()
        
        #when GPS lose its position, the return is zero. So, I check if
        #the info received is zero. If not, is an information.
        if readline.find('GGA') > 0:
            msg = pynmea2.parse(readline)
            self.Timestamp = msg.timestamp
            
            if msg.lat_dir == "W":
                self.Lat = "-" + str(msg.lat) # -8.0000
            else:
                self.Lat = "+" + str(msg.lat) # +8.0123

            if msg.lon_dir == "S":
                self.Lon = "-" + msg.lon
            else:
                self.Lon = "+" + msg.lon

            self.Altitude = str(msg.altitude) + str(msg.altitude_units)
            self.Satellites = msg.num_sats
            ## OK return
            return 0 

        else:
            ## GPS has lose the conection
            return -1   

