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
    def __init__(self,precisionNumber=4):
        self.TimeZone = -3
        #digits after "," precision
        self.precisionNumber = precisionNumber 
        #main infos returned from GPS board
        self.Timestamp = "0"
        self.Lat = "0"
        self.Lon = "0"
        self.Altitude = "0"
        self.Satellites = "0"
        self.Timestamp = "0"
        self.Velocidade = "0"

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
            msg.Lat = self.__fixCoordinates(msg.lat)
            msg.Lon = self.__fixCoordinates(msg.lon)

            if msg.lat_dir == "S":
                self.Lat = "-" + str(msg.Lat) # -8.0000
            else:
                self.Lat = "+" + str(msg.Lat) # +8.0123

            if msg.lon_dir == "W":
                self.Lon = "-" + str(msg.Lon)
            else:
                self.Lon = "+" + str(msg.Lon)

            self.Altitude = str(msg.altitude) + str(msg.altitude_units)
            self.Satellites = msg.num_sats
            ## OK return
            return 0 

        elif readline.find('VTG') > 0:
            velocidadeGPS = readline.split(",")
            #velocity in Km/h
            self.Velocidade = str(velocidadeGPS[7])

        else:
            ## GPS has lose the conection
            return -1   

    def __fixCoordinates(self,coordinates):
        
        integerPart = float(coordinates)/100
        integerPart = str(integerPart)
        x = integerPart.split(".")

        parteInteira = int(x[0])
        outraParte = x[1]
        minutos = outraParte[:2]
        minutosParteII = outraParte[2:]
        outraParte = float(minutos + "." + minutosParteII)/60

        final = parteInteira + outraParte
        final = float("{0:.{1}f}".format(final,self.precisionNumber))
        return final

