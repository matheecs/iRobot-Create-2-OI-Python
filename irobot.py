import serial
import time
from struct import *

def wakeRobot(ser):
    ser.rts = True
    time.sleep(0.1)
    ser.rts = False
    time.sleep(1)

def resetRobotAndWait(ser):
    ser.reset_input_buffer()
    ser.write('\x07')
    sBuffer = "dummy string"
    while len(sBuffer) is not 0:
        sBuffer = ser.readline()
        print sBuffer.strip()

irobot = serial.Serial(port='/dev/tty.usbserial-DA01NU2A', 
    baudrate=115200, timeout = 3.0)
wakeRobot(irobot)
irobot.write(pack('B',128))
print "Start iRobot..."

irobot.write(pack('B',131))
time.sleep(.1)

irobot.write(pack('B'+'c'*4, 164,'1','2','3','4'))
irobot.write(pack('B'*3+'cB'*5,140,0,5,'C',16,'H',24,'J',8,'L',16,'O',32))
irobot.write(pack('B'*2,141, 0))
time.sleep(1.6)


# '>h', '>H'
irobot.write(pack('B'*2,142, 21))
print "char:", unpack('B',irobot.read(1))
irobot.write(pack('B'*2,142, 22))
print "volt:", unpack('>H',irobot.read(2))
irobot.write(pack('B'*2,142, 23))
print "curr:", unpack('>h',irobot.read(2))
irobot.write(pack('B'*2,142, 24))
print "temp:", unpack('b',irobot.read(1))
irobot.write(pack('B'*2,142, 25))
print "batt:", unpack('>H',irobot.read(2))
irobot.write(pack('B'*2,142, 26))
print "Batt:", unpack('>H',irobot.read(2))

irobot.write(pack('B'*2,142, 3))
print "G3:", unpack('>BHhbHH',irobot.read(10))

irobot.write(pack('B'*2,142, 107))
print "G107:", unpack('>h'+'h'*3+'B',irobot.read(9))

irobot.write(pack('B',128))
print "Pause iRobot..."
irobot.close()
