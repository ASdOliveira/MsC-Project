from I2C_driver import *
import time


ADDRESS = 0x1D

#registers
STATUS = 0x00
OUT_X_MSB = 0x01
OUT_X_LSB = 0x02
OUT_Y_MSB = 0x03
OUT_Y_LSB = 0x04
OUT_Z_MSB = 0x05
OUT_Z_LSB = 0x06
SYSMOD = 0x0B
INT_SOURCE = 0x0C
WHO_AM_I = 0x0D
XYZ_DATA_CFG = 0x0E
HP_FILTER_CUTOFF = 0x0F
PL_STATUS = 0x10
PL_CFG = 0x11
PL_COUNT = 0x12
PL_BF_ZCOMP = 0x13
P_L_THS_REG = 0x14
FF_MT_CFG = 0x15
FF_MT_SRC = 0x16
FF_MT_THS = 0x17
FF_MT_COUNT = 0x18
TRANSIENT_CFG = 0x1D
TRANSIENT_SRC = 0x1E
TRANSIENT_THS = 0x1F
TRANSIENT_COUNT = 0x20
PULSE_CFG = 0x21
PULSE_SRC = 0x22
PULSE_THSX = 0x23
PULSE_THSY = 0x24
PULSE_THSZ = 0x25
PULSE_TMLT = 0x26
PULSE_LTCY = 0x27
PULSE_WIND = 0x28
ASLP_COUNT = 0x29
CTRL_REG1 = 0x2A
CTRL_REG2 = 0x2B
CTRL_REG3 = 0x2C
CTRL_REG4 = 0x2D
CTRL_REG5 = 0x2E
OFF_X = 0x2F
OFF_Y = 0x30
OFF_Z = 0x31

class acelerometer:
    def __init__(self, ADDR, SCALE=2, ODR=800):
        self.i2c = i2c_device(ADDR)
        self.scale = SCALE
        self.odr = ODR
        self.x = 0
        self.y = 0
        self.z = 0
        
        #put in stand by mode
        self.standby()
        self.setScale(SCALE)
        self.setOdr(ODR)
        self.setupReadPosition()
        self.active()


    def standby(self):
        regVal = self.i2c.read_data(CTRL_REG1)
        regVal = regVal & ~(0x01) #Clear the last bit
        self.i2c.write_cmd_arg(CTRL_REG1,regVal)

    def setScale(self,scale):
        self.scale = scale
        regVal = self.i2c.read_data(XYZ_DATA_CFG)
        
        if scale == 2:
            mask = 0x00
        elif scale == 4:
            mask = 0x01
        elif scale == 8:
            mask = 0x02
        else:
            #error!!

            return
        
        regVal = regVal | mask
        self.i2c.write_cmd_arg(XYZ_DATA_CFG,regVal)

    def setOdr(self,odr):
        self.odr = odr
        regVal = self.i2c.read_data(CTRL_REG1)
    
        if odr == 800:
            mask = 0x00
        elif odr == 400:
            mask = 0x20
        elif odr == 200:
            mask = 0x40
        elif odr == 100:
            mask = 0x60
        elif odr == 50:
            mask = 0x80
        elif odr == 12:
            mask = 0xA0
        elif odr == 6:
            mask = 0xC0
        elif odr == 1:
            mask = 0xE0
        else:
            return #error!!
        
        regVal = (regVal & 0x1F) | mask #bitmask
        
        self.i2c.write_cmd_arg(CTRL_REG1,regVal)

    def active(self):
        regVal = self.i2c.read_data(CTRL_REG1)
        regVal = regVal | 0x01
        self.i2c.write_cmd_arg(CTRL_REG1,regVal)

    def read(self):
        data = self.i2c.read_i2c_block_data(OUT_X_MSB,6)

        self.x = float((data[0] * 256 + data[1]) / 16)
        self.x = self.__math(self.x,self.scale)

        self.y = float((data[2] * 256 + data[3]) / 16)
        self.y = self.__math(self.y,self.scale)
        
        self.z = float((data[4] * 256 + data[5]) / 16)
        self.z = self.__math(self.z,self.scale)

    def __math(self, value, scale):
        if value > 2047:
            value -= 4096
        value = float(value/2048) * scale
        return value

    def setupReadPosition(self):
        regVal = self.i2c.read_data(PL_CFG)
        self.i2c.write_cmd_arg(PL_CFG,(regVal | 0x40))
        self.i2c.write_cmd_arg(PL_COUNT,0x50)


    def readPosition(self):
        regVal = self.i2c.read_data(PL_STATUS)
        if((regVal & 0x40) == 1):
            position = "Flat"
        else:
            regVal = (regVal & 0x06) >> 1

            if regVal == 0x00:
                position = "Portrait UP"
            elif regVal == 0x01:
                position = "Portrait Down"
            elif regVal == 0x02:
                position = "Landscape Right"
            elif regVal == 0x03:
                position = "Landscape Left"

        return position

acelerometro = acelerometer(ADDRESS)

while True:
    acelerometro.read()
    position = acelerometro.readPosition()
    print (position)
    #print(str(acelerometro.x) + " " + str(acelerometro.y) + " " + str(acelerometro.z))
    
    time.sleep(0.3)