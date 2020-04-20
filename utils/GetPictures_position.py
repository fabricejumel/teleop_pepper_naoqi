#! /usr/bin/env python
# -*- encoding: UTF-8 -*-


import qi
import argparse
import sys
import time
import signal
import almath
import json

def main(session,x,y,theta,dataset):
    # Get the service ALTabletService.

    try:
	basicAwareness=session.service("ALBasicAwareness")
	basicAwareness.setEnabled(False)
	almotion=session.service("ALMotion")
	almotion.setStiffnesses("Head", 1.0)
	alphoto=session.service("ALPhotoCapture")
	alphoto.setResolution(4)
	alphoto.setPictureFormat("jpg")
    
  
        #tabletService = session.service("ALTabletService")
        #tabletService.loadApplication("SimpleWeb")
        #tabletService.showWebview()

    except Exception, e:
        print "Error was: ", e

    list = [[115,0], [110,0]]	

    names            = ["HeadYaw","HeadPitch"]
    angles = [0,0]
    try:
	almotion.setAngles(names,angles,0.1)
    except Exception, e:
        print "Error was: ", e
    dir="/data/home/nao/dataset/D"+dataset
    imbase='IM'
    details = {  
    'dataset': dataset,
    'x': x,
    'y': y,
    'theta' : theta,
    'yaw': 0.0,
    'pitch':0.0,
    'divers': 'none',
    }
    #name=json.dumps(details,separators=(',', ':'))
    #alphoto.takePictures(1, "/home/nao/images", name)
    detailsname=details
    
    for j in range(-40,36,5):
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
	print("end")



    # Getting the service ALDialog
    #try:
    	#ALDialog = session.service("ALDialog")
        #ALDialog.resetAll()
    	#ALDialog.setLanguage("English")




    	# Loading the topics directly as text strings
    	#topic_name = ALDialog.loadTopic("/home/nao/.local/share/PackageManager/apps/SimpleWeb/simple_en.top")
    	#topic_name = ALDialog.loadTopic("/home/fabrice/nts-example/SimpleWeb/simple_en.top")


    	# Activating the loaded topics
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
    parser.add_argument("--x", type=int, default=100,
                        help="x distance to shelve")
    parser.add_argument("--y", type=int, default=0,
                        help="y distance to shelve")
    parser.add_argument("--theta", type=int, default=0,
                        help="theta orientation to shelve") 
    parser.add_argument("--dataset", type=str, default="00001",
                        help="theta orientation to shelve")             
    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session,args.x,args.y,args.theta,args.dataset)

