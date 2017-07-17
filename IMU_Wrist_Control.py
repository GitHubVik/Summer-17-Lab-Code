import argparse
import numpy
import time
import rospy
 
import baxter_interface
import baxter_external_devices
 
from baxter_interface import CHECK_VERSION
import serial 



ser = serial.Serial('/dev/ttyACM0', 115200)




def forearm_control():
    right = baxter_interface.Limb('right')
    rj = right.joint_names()
    offset = calibrate()
    right.set_joint_positions({rj[0]: 0.0})
    while True:
        sensorValues = ser.readline()
        if(is_float(sensorValues)): 
            ypr = sensorValues.split()
            yaw = -numpy.radians(float(ypr[0]))
            pitch = numpy.radians(float(ypr[1])) - offset
            roll = numpy.radians(float(ypr[2]))
            print yaw
            #print(str(yaw) + ", " + str(pitch) + ", " + str(roll))
            set_j(right, rj[3], pitch)
            #set_j(right, rj[4], roll)
            

def is_float(s):
    try:
        float(s.split()[0])
        float(s.split()[1])
        float(s.split()[2])
        return True
    except ValueError:
        return False
    except IndexError:
        return False


def calibrate():

    time.sleep(3)
    sensorValues = ser.readline()
    return numpy.radians(float(sensorValues.split()[1]))

def set_j(limb, joint_name, value):
        
        joint_command = {joint_name: value}
        limb.set_joint_positions(joint_command)



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