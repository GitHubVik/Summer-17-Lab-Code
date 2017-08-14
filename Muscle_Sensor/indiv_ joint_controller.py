import argparse
import numpy
import rospy
 
import baxter_interface
import baxter_external_devices
 
from baxter_interface import CHECK_VERSION




def angle_sender():
	right = baxter_interface.Limb('right')
	rj = right.joint_names()



	print("This is a test for writing individual joint angles to Baxter")
	joint_angle = input("What angle would you like the joint to move to, in degrees?: ")
	limb = right

	
	limb.move_to_joint_positions({rj[5]:joint_angle})



def main():
    """TEST PROGRAM TO CONTROL INDIVIDUAL JOINT VALUES
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
	 
    angle_sender()    
    print("Done.")
 
 
if __name__ == '__main__':
    main()