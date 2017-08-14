import argparse
import numpy
import rospy
 
import baxter_interface
import baxter_external_devices
 
from baxter_interface import CHECK_VERSION
import serial 



ser = serial.Serial('/dev/ttyACM0', 9600)


#************************************************************

def gripper_control():
    print("CALIBRATING.....")
    left = baxter_interface.Gripper('left')
    left.calibrate()
    print("CALIBRATION COMPLETED")
    
    while True:                 # Wait for keyboard interrupt for now; press ctrl+c to exit
        sensorValue = ser.readline()
        print(sensorValue)

        if(sensorValue.strip() != ""):
            if(int(sensorValue) < 90):
                #print("open")
                left.open()

            if(int(sensorValue) >= 100):
                #print("close")
                left.close()



#*************************************************************

def main():
    """TEST PROGRAM TO CONTROL GRIPPER WITH MUSCLE SENSOR FROM ARDUINO
   """
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
    gripper_control()
    print("Done.")
 
 
if __name__ == '__main__':
    main()