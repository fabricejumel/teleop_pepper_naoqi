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

def deadzone(low, value):
    if abs(value) < low:
        return 0
    else:
        return(value) 


def main(session,joy_id,dir,name,quality):
    # Get the service ALTabletService.
    try:
        basicAwareness=session.service("ALBasicAwareness")
        basicAwareness.setEnabled(False)
        almotion=session.service("ALMotion")
        altext=session.service("ALTextToSpeech")
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
    almotion.rest()
    name = "All"
    enable  = False
    almotion.setExternalCollisionProtectionEnabled(name, enable)
    almotion.setOrthogonalSecurityDistance(0.01)
    almotion.setTangentialSecurityDistance(0.01)
    almotion.wakeUp()
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

    
    vrecorder.setFrameRate(10.0)
    vrecorder.setResolution(quality) # 0 (QQVGA), 1 (QVGA) or 2 (VGA) , 2 Set resolution to VGA (640 x 480)

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
    OMNI=0
    CLASSIQUE=1
    STOP = -1
    mode = CLASSIQUE
    start=0
    stop=0
    button_stop_old=0
    button_start_old=0
    while not done:


        #raw_input("\n Press Enter to continue:")

        pygame.event.get()
        name = joystick.get_name()
        axes = joystick.get_numaxes()
        epsilonyaw=0.04
        minyawRAD=-2
        maxyawRAD=2

        epsilonpitch=0.04
        minpitchRAD=-0.33
        maxpitchRAD=0.33
        
        axis_yaw = (-1)*joystick.get_axis(3)
        axis_pitch = joystick.get_axis(4)

        angle_yaw=angles[0]+epsilonyaw*axis_yaw
        angle_yaw=bound(minyawRAD,maxyawRAD,angle_yaw)

        angle_pitch=angles[1]+epsilonpitch*axis_pitch
        angle_pitch=bound(minpitchRAD,maxpitchRAD,angle_pitch)



        deadzone_front=0.05
        deadzone_slide=0.05

        limit_front=0.5
        limit_slide=1
        axis_front =(-1)*joystick.get_axis(1)
        axis_slide = (-1)*joystick.get_axis(0)
        xdot=deadzone(deadzone_front,axis_front)*limit_front
        slidedot=deadzone(deadzone_slide,axis_slide)*limit_slide

        if mode==CLASSIQUE:
            thetadot=slidedot
            ydot=0
            hat0 = joystick.get_hat(0)
            if hat0 != (0,0):
                limit_omni=1
                xdot=hat0[1]*limit_omni
                ydot=(-1)*hat0[0]*limit_omni
            almotion.moveToward(xdot, ydot, thetadot)

        elif mode==OMNI:
            ydot=slidedot

            almotion.moveToward(xdot, ydot, 0 )
            
            

            almotion.moveToward(x_dot, y_dot, 0 )

        elif mode==STOP:
            almotion.moveToward(0, 0, 0 )
       

        angles = [angle_yaw, angle_pitch]
        print("angles:")
        print(angles)
        almotion.setAngles(names,angles,0.1)
    


        buttons = joystick.get_numbuttons()
        button_start = joystick.get_button(3)
        if button_start and ( button_start != button_start_old):
            start=1
        if start==1:
            start=0
            altext.say("Record Video Start")
            name='PEPPER_'+(str((datetime.now())).replace(' ','-'))[:-7]
            vrecorder.startRecording(dir, name)
        button_start_old=button_start


        button_stop = joystick.get_button(1)
        if button_stop and (button_stop != button_stop_old):
            stop=1
        if stop==1:
            stop=0
            vrecorder.stopRecording()
            altext.say("Record Video Stop")
        button_stop_old=button_stop

       


 

 

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

