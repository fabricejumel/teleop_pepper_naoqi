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

def main(session,dir,name,quality):
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
	

    names            = ["HeadYaw","HeadPitch"]
    angles = [0,0]
    try:
	almotion.setAngles(names,angles,0.1)
    except Exception, e:
        print "Error was: ", e
    alphoto.takePictures(1, dir, name)

    vrecorder.setFrameRate(10.0)
    vrecorder.setResolution(quality) # 2 Set resolution to VGA (640 x 480)

    vrecorder.startRecording(dir, name)
    print "Video record started."

    time.sleep(5) # We'll save a 5 second video record in /home/nao/recordings/cameras/

    videoInfo = vrecorder.stopRecording()
    print "Video was saved on the robot: ", videoInfo[1]
    print "Total number of frames: ", videoInfo[0]
    
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

    #try:
        #raw_input("\n Press Enter when finished:")
    #finally:
        # stopping the dialog engine
        #ALDialog.unsubscribe('simple')

        # Deactivating the topic
        #ALDialog.deactivateTopic(topic_name)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        #ALDialog.unloadTopic(topic_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    dir="/data/home/nao/dataset/"
    name='PEPPER_'+str((datetime.now())).replace(' ','-')
    parser.add_argument("--dir", type=str, default=dir,
                        help="directory")
    parser.add_argument("--name", type=str, default=name,
                        help="name of the generated file")
    parser.add_argument("--quality", type=int, default=4,
                        help="name of the generated file")
            
    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session,args.dir,args.name,args.quality)

