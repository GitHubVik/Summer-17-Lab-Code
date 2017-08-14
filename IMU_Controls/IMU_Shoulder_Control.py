import argparse
import numpy
import time
import rospy
 
import baxter_interface
import baxter_external_devices
 
from baxter_interface import CHECK_VERSION
import serial 



ser = serial.Serial('/dev/ttyACM0', 9600)
y1 = 0
p1 = 1
r1 = 2
y2 = 3
p2 = 4
r2 = 5


def forearm_control():
    right = baxter_interface.Limb('right')
    rj = right.joint_names()
    offsets = offset()

    while True:
        sensorValues = ser.readline()
        if(is_float(sensorValues)): 
            yprtot = ypr_calc(offsets)  
            set_j(yprtot)
            #print(str(yaw) + ", " + str(pitch) + ", " + str(roll))
            

#yaw = numpy.radians(float(ypr[0])) - offsety
#pitch = numpy.radians(float(ypr[1])) - offsetp
#roll = numpy.radians(float(ypr[2])) - offsetr

            
def ypr_calc(offsets):

    msg = recvFromArduino()
    
    yprsnew = msg.split()
    yprs = [float(i) for i in yprsnew]
    
    
    yprs1 = [yprs[0]-offsets[0], yprs[1]-offsets[1], yprs[2]-offsets[2]]
    yprs2 = [yprs[3]-offsets[3], yprs[4]-offsets[4], yprs[5]-offsets[5]]
    yprs2 = list(numpy.array(yprs2)-numpy.array(yprs1))
    yprtot = [yprs1, yprs2]
    print(yprtot)
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
        float(s.split()[6])
        float(s.split()[7])

        return True
    except ValueError:
        return False
    except IndexError:
        return False

#****************

def calibrate(s):
    sensorValues = ser.readline()
    print sensorValues
    print("SensorValues.split:" )
    print sensorValues.split()
    return float(sensorValues.split()[s])


#****************


def offset():
    time.sleep(10)
    sensorValues = ser.readline()
    offsets = []
    offsets.append(calibrate(y1))
    offsets.append(calibrate(p1))
    offsets.append(calibrate(r1))
    offsets.append(calibrate(y2))
    offsets.append(calibrate(p2))
    offsets.append(calibrate(r2))
    return offsets

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


def main():
    """PROGRAM TO CONTROL THE WRIST PITCH AND ROLL FROM IMU ON HUMAN HAND  """
    

    epilog = """
See help inside the example with the '?' key for key bindings.
   """
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__,
                                     epilog=epilog)
    parser.parse_args(rospy.myargv()[1:])
 
    print("Initializing node... ")
    rospy.init_node("rsdk_joint_angle_test")
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled
    def clean_shutdown():
        print("\nExiting example...")
        if not init_state:
            print("Disabling robot...")
            rs.disable()


    rospy.on_shutdown(clean_shutdown)

    print("Enabling robot... ")
    rs.enable()
    forearm_control()
    print("Done.")
 
 
if __name__ == '__main__':
    main()