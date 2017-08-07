import argparse
import numpy
import time
 
import serial 



ser = serial.Serial('/dev/ttyACM0', 9600)


y1 = 0      #\
p1 = 1      # \
r1 = 2      #  \   Each of the numbers corresponds to each of the roll, pitch, and yaw positions in the recieved lists
y2 = 3      #  /
p2 = 4      # /
r2 = 5      #/


#right = baxter_interface.Limb('right')
#rj = right.joint_names()

            #set_j(yprtot)
            #print(str(yaw) + ", " + str(pitch) + ", " + str(roll))
            

#yaw = numpy.radians(float(ypr[0])) - offsety
#pitch = numpy.radians(float(ypr[1])) - offsetp
#roll = numpy.radians(float(ypr[2])) - offsetr


def offsetter(num):                                #Creates offsets in order for calibration and "zeroing" of baxter arm     
    sensorValues = recvFromArduino()
    counter = 0
    offsets = []
    while(not is_float(sensorValues)):    
        sensorValues = recvFromArduino()
        
    while(is_float(sensorValues)):
        if counter == 1000:
            offsets = []
            offsets.append(calibrate(y1))
            offsets.append(calibrate(p1))
            offsets.append(calibrate(r1))
            offsets.append(calibrate(y2))
            offsets.append(calibrate(p2))
            offsets.append(calibrate(r2))
            print(offsets)
            return offsets
        else:
            counter = counter+ 1
            sensorValues = recvFromArduino()

def ypr_calc(offsets):                                                      #      Calculates each of the yaw, pitch, and roll values from the arduino
    msg = recvFromArduino()
    #print msg.split()                                                 #      and organizes them into a readable format to send to Baxter
    if is_float(msg) == True:
        yprsnew = msg.split()
        yprs = [float(i) for i in yprsnew]
        yprs1 = [yprs[0]-offsets[0], yprs[1]-offsets[1], yprs[2]-offsets[2]]    #       Subtracts the offsets from the recieved values
        yprs2 = [yprs[3]-offsets[3], yprs[4]-offsets[4], yprs[5]-offsets[5]]    #       "                                             "
        yprs3 = list(numpy.array(yprs2)-numpy.array(yprs1))                     #       Subtracts the values from the second IMU from the first, in order to avoid any double movements 
        yprtot = [yprs1, yprs3]
        #print(yprtot)
        return yprtot

        

#****************


def joint_finder(yprtot):
    if not yprtot[0]:
        ypr = [rj[0], rj[1], rj[2]]
    else:
        ypr = [rj[3], rj[4]]
    return ypr


#****************


def is_float(s):
    try:
        float(s.split()[0])
        float(s.split()[1])
        float(s.split()[2])
        float(s.split()[3])
        float(s.split()[4])
        float(s.split()[5])
  

        return True
    except ValueError:
        return False
    except IndexError:
        return False

#****************

def calibrate(s):
    sensorValues = recvFromArduino()
    #print("SensorValues.split:" )
    return float(sensorValues.split()[s])


#****************



def set_j(yprtot):
    right = baxter_interface.Limb('right')

    rj = right.joint_names()
    yprs1 = yprtot[0]
    yprs2 = yprtot[1]    
    joint_command = {rj[0]:yprs1[0], rj[1]:yprs1[1], rj[2]:yprs1[2], rj[3]:yprs2[1], rj[4]:yprs2[2] }
    right.set_joint_positions((joint_command))


def recvFromArduino():
  global startMarker, endMarker
  
  ck = ""
  x = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  while  ord(x) != startMarker: 
    x = ser.read()
  
  # save data until the end marker is found
  while ord(x) != endMarker:
    if ord(x) != startMarker:
      ck = ck + x 
      byteCount += 1
    x = ser.read()
  
  return(ck)


#****************************************************************************************************
startMarker = 60
endMarker = 62

offsets = list()
offsets = offsetter(2)
while True:
    yprtot = ypr_calc(offsets)  
    print(yprtot)