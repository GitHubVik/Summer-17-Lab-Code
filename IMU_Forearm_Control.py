import argparse
import numpy
import rospy
 
import baxter_interface
import baxter_external_devices
 
from baxter_interface import CHECK_VERSION
import serial 



ser = serial.Serial('/dev/ttyACM1', 115200)




def forearm_control():
    right = baxter_interface.Limb('right')
    rj = right.joint_names()
    while True:
        sensorValues = ser.readline()
        if(is_float(sensorValues)): 
            ypr = sensorValues.split()
            yaw = numpy.radians(float(ypr[0]))
            pitch = numpy.radians(float(ypr[1]))
            roll = numpy.radians(float(ypr[2]))
            print pitch
            #print(str(yaw) + ", " + str(pitch) + ", " + str(roll))
            right.set_joint_positions({rj[5]:pitch}, {rj[6]:roll})
            #right.set_joint_positions({rj[6]:roll})

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