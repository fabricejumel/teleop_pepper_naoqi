#! /usr/bin/env python
# -*- encoding: UTF-8 -*-


import qi
import argparse
import sys
import time
import signal
import almath
import json
from datetime import datetime
import pygame
import os
import sys

def bound(low, high, value):
    return max(low, min(high, value))


def main(session,joy_id,dir,name,quality):
    # Get the service ALTabletService.
    try:
        basicAwareness=session.service("ALBasicAwareness")
        basicAwareness.setEnabled(False)
        almotion=session.service("ALMotion")
        almotion.setStiffnesses("Head", 1.0)
        alphoto=session.service("ALPhotoCapture")
        alphoto.setResolution(4)
        alphoto.setPictureFormat("jpg")
        vrecorder=session.service("ALVideoRecorder")


        
    #tabletService = session.service("ALTabletService")
    #tabletService.loadApplication("SimpleWeb")
    #tabletService.showWebview()

    except Exception, e:
        print "Error was: ", e
	

    names = ["HeadYaw","HeadPitch"]
    angles = [0,0]
    almotion.setAngles(names,angles,0.1)
    # try:
	# almotion.setAngles(names,angles,0.1)
    # except Exception, e:
    #     print "Error was: ", e

    # for i in range (0,8):
    #     alphoto.setResolution(i)
    #     name2=name + ':RES:' + str(i)
    #     alphoto.takePictures(1, dir, name2)

    
    # vrecorder.setFrameRate(10.0)
    # vrecorder.setResolution(quality) # 0 (QQVGA), 1 (QVGA) or 2 (VGA) , 2 Set resolution to VGA (640 x 480)

    # vrecorder.startRecording(dir, name)
    # print "Video record started."

    # time.sleep(5) # We'll save a 5 second video record in /home/nao/recordings/cameras/

    # videoInfo = vrecorder.stopRecording()
    # print "Video was saved on the robot: ", videoInfo[1]
    # print "Total number of frames: ", videoInfo[0]
    
    """     for j in range(-40,36,5):
	    first=1
	    for i in range(-20,20,5):
		angles[0]=i*almath.TO_RAD
		angles[1]=j*almath.TO_RAD
		almotion.setAngles(names,angles,0.1)
		if first==1:
			first=0
			time.sleep(2)
		detailsname["yaw"]=i
		detailsname["pitch"]=j
		#time.sleep(0.5)
		name=json.dumps(details,separators=(',', ':'))
		print(name)
		alphoto.takePictures(1, dir, name)
    try:
	raw_input("\n Press Enter when finished:")
    finally:
	print("end") """



    # Getting the service ALDialog
    #try:
    	#ALDialog = session.service("ALDialog")
        #ALDialog.resetAll()
    	#ALDialog.setLanguage("English")
    	#ALDialog.activateTopic(topic_name)


    	# Starting the dialog engine - we need to type an arbitrary string as the identifier
    	# We subscribe only ONCE, regardless of the number of topics we have activated
    	#ALDialog.subscribe('simple')

    #except Exception, e:
        #print "Error was: ", e

    pygame.init()
    # Set the width and height of the screen [width,height]

    # Loop until the user clicks the c  lose button.
    done = False 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()  
    # Initialize the joysticks
    pygame.joystick.init() 
    # Get ready to print


    joystick = pygame.joystick.Joystick(joy_id)
    joystick.init()

    while not done:


        #raw_input("\n Press Enter to continue:")

        pygame.event.get()
        name = joystick.get_name()
        axes = joystick.get_numaxes()
        epsilonyaw=0.02
        minyawRAD=-2
        maxyawRAD=2

        epsilonpitch=0.04
        minpitchRAD=-0.33
        maxpitchRAD=0.33
        

        axis0 = joystick.get_axis(3)
        axis1 = joystick.get_axis(4)

        angle_yaw=angles[0]+epsilonyaw*axis0
        angle_yaw=bound(minyawRAD,maxyawRAD,angle_yaw)

        angle_pitch=angles[1]+epsilonpitch*axis1
        angle_pitch=bound(minpitchRAD,maxpitchRAD,angle_pitch)


        

        angles = [angle_yaw, angle_pitch]
        print("angles:")
        print(angles)
        almotion.setAngles(names,angles,0.1)
        print(axis0)


        buttons = joystick.get_numbuttons()
        button0 = joystick.get_button(0)
        button1 = joystick.get_button(1)
        print(button0)


        hats = joystick.get_numhats()

        hat0 = joystick.get_hat(0)
        print(hat0)

        clock.tick(30)
    
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

























    try:
            raw_input("\n Press Enter when finished:")
    finally:
        almotion.setStiffnesses("Head", 0.1)
        # stopping the dialog engine
        # ALDialog.unsubscribe('simple')
        # Deactivating the topic
        # ALDialog.deactivateTopic(topic_name)
        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        # ALDialog.unloadTopic(topic_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    dir="/data/home/nao/dataset/"
    name='PEPPER_'+(str((datetime.now())).replace(' ','-'))[:-7]
    parser.add_argument("--dir", type=str, default=dir,
                        help="directory")
    parser.add_argument("--name", type=str, default=name,
                        help="name of the generated file")
    parser.add_argument("--quality", type=int, default=2,
                        help="name of the generated file")
    parser.add_argument("--joy", type=int, default=0,
                        help=" 0 is  use for /dev/input/js0")      
    args = parser.parse_args()
    session = qi.Session()
    
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    main(session,args.joy,args.dir,args.name,args.quality)

