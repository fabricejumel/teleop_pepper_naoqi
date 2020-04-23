Parameter ID Name |	ID Value  |	Description
----------------- | --------- | -------------
AL::kQQQQVGA |	8 |	Image of 40*30px
AL::kQQQVGA |	7 |	Image of 80*60px
AL::kQQVGA |	0 |	Image of 160*120px
AL::kQVGA |	1 |	Image of 320*240px
AL::kVGA |	2 |	Image of 640*480px
AL::k4VGA |	3 |	Image of 1280*960px
AL::k16VGA |	4 |	Image of 2560*1920px




Motion range
Joint name 	Motion 	Range (degrees) 	Range (radians)
HeadYaw 	Head joint twist (Z) 	-119.5 to 119.5 	-2.0857 to 2.0857
HeadPitch 	Head joint front and back (Y) 	-38.5 to 29.5 	-0.6720 to 0.5149
Click the joint name to see all related ALMemory key names.

Anti collision limitation

Due to potential shell collision at the head level, the Pitch motion range is limited according to the Yaw value.
HeadYaw 	HeadPitch Min 	HeadPitch Max 	  	HeadYaw 	HeadPitch Min 	HeadPitch Max
(degrees) 	(radians)
-119.52 	-25.73 	18.91 	  	-2.086017 	-0.449073 	0.330041
-87.49 	-18.91 	11.46 	-1.526988 	-0.330041 	0.200015
-62.45 	-24.64 	17.19 	-1.089958 	-0.430049 	0.300022
-51.74 	-27.50 	18.91 	-0.903033 	-0.479965 	0.330041
-43.32 	-31.40 	21.20 	-0.756077 	-0.548033 	0.370010
-27.85 	-38.50 	24.18 	-0.486074 	-0.671951 	0.422021
0.0 	-38.50 	29.51 	0.000000 	-0.671951 	0.515047
27.85 	-38.50 	24.18 	0.486074 	-0.671951 	0.422021
43.32 	-31.40 	21.20 	0.756077 	-0.548033 	0.370010
51.74 	-27.50 	18.91 	0.903033 	-0.479965 	0.330041
62.45 	-24.64 	17.19 	1.089958 	-0.430049 	0.300022
87.49 	-18.91 	11.46 	1.526988 	-0.330041 	0.200015
119.52 	-25.73 	18.91 	2.086017 	-0.449073 	0.330041

test fj:
pepper:
gst-launch-0.10 -v v4l2src device=/dev/video0 ! 'video/x-raw-yuv,width=320, height=240,framerate=5/1' ! ffmpegcolorspace ! jpegenc ! rtpjpegpay ! udpsink host=192.168.1.27 port=3000
PC :    
gst-launch-0.10 -v udpsrc port=3000 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink

    gst-launch-0.10 -v v4l2src device=/dev/video-top ! video/x-raw-yuv,width=640,height=480,framerate=30/1 ! ffmpegcolorspace ! jpegenc ! multipartmux! tcpserversink port=3000

... and then you can open the stream from your computer, for example with vlc:

    vlc tcp://ip.of.the.robot:3000



    -------------------


    Paco Dupont 	
09/03/2017
Traduire le message en français  
Hello,

after some weeks digging ROS with Pepper robot, I wasn't able to achieve good camera streaming with naoqi for SLAM purpose or image processing and ran in a lots of trouble with the camera stream which were very slow and with a low quality (10fps in QVGA, dropping to 4-5fps in VGA). This rate and quality added to the poor precision of the depth sensor makes Pepper pretty unusable for visual SLAM approach (like RTABMAP).

I tried a new approach and managed to establish a stable stream at 24fps in VGA for both front and bottom camera !! :

I used gstreamer to create an UDP (+RTP) stream of the front (/dev/video0) and bottom (/dev/video1) camera from Pepper, the stream is then retrieved on the PC_HOST with gscam and remapped in /pepper_robot/camera tree.

PEPPER <--------- (UDP + RTP jpeg payload encoding) -----------> PC_HOST


Step by step procedure :

1) Disable autonomous life :
First of all you have to disable autonomous life behavior on Pepper robot, go to Pepper web page > Advanced configuration > Alive by default OFF
Disabling autonomous life manually after robot startup doesn't work ! The autonomous life behavior doesn't properly release the video device and can mess with the camera buffer, and the camera driver do not keep you from opening the device from multiple process (no EBUSY error).
If you don't want to disable autonomous life you can only use the camera bottom (i.e. /dev/video1).

2) Launch gstreamer on Pepper:
SSH to Pepper and run those command (it's possible to add a script to autoload.ini), change PC_HOST by the IP of remote computer running ROS, you can chose a different port if you prefer.
You can also change the resolution if needed : VGA 640*480, QVGA 320*240

Camera front :
gst-launch-0.10 -v v4l2src device=/dev/video0 ! 'video/x-raw-yuv,width=640, height=480,framerate=30/1' ! ffmpegcolorspace ! jpegenc ! rtpjpegpay ! udpsink host=PC_HOST port=3000

Camera bottom:
gst-launch-0.10 -v v4l2src device=/dev/video1 ! 'video/x-raw-yuv,width=640, height=480,framerate=30/1' ! ffmpegcolorspace ! jpegenc ! rtpjpegpay ! udpsink host=PC_HOST port=3001




3) Test the pipeline on PC_HOST :
You can immediately test the pipeline created above by launching those command on the PC_HOST:

Camera front:
gst-launch-0.10 -v udpsrc port=3001 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink

Camera bottom:
gst-launch-0.10 -v udpsrc port=3000 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink

This pipeline is compatible with gst-launch-1.10 and gst-launch-0.10.



4) Merge ROS, Gstreamer and Naoqi :
Clone the fork of gscam and pepper_bringup in a catkin workspace and checkout dev branch :

git clone https://github.com/PacoDu/gscam
cd gscam
git checkout dev

git clone https://github.com/PacoDu/pepper_robot
cd pepper_robot
git checkout dev

catkin_make and source devel/setup.bash

You can now run :
(Adapt variable to you environment)
roslaunch pepper_bringup pepper_gst.launch nao_ip:="$NAO_IP" roscore_ip:="$ROSCORE_IP" network_interface:="$NETWORK_INTERFACE" PORT_CAMERA_FRONT:="$CAMERA_PORT0" PORT_CAMERA_BOTTOM:="$CAMERA_PORT1" | grep -v "LogMessage"




5) Result :
You can run rviz and select /pepper_robot/camera/front/image_raw in raw or compressed mode.

$ rostopic hz /pepper_robot/camera/front/image_raw
subscribed to [/pepper_robot/camera/front/image_raw]
average rate: 24.034
    min: 0.037s max: 0.044s std dev: 0.00165s window: 23

$ rostopic hz /pepper_robot/camera/front/image_raw/compressed
subscribed to [/pepper_robot/camera/front/image_raw/compressed]
average rate: 24.002
    min: 0.040s max: 0.044s std dev: 0.00076s window: 23

$ rostopic bw /pepper_robot/camera/front/image_raw/compressed
subscribed to [/pepper_robot/camera/front/image_raw/compressed]
average: 449.19KB/s
    mean: 18.57KB min: 18.53KB max: 18.65KB window: 23

An other advantage is that you can now pass a calibration file for the camera (c.f. perception_gst.launch.xml param camera_info_url) located in pepper_bringup/config instead of default calibration written in naoqi driver source code.



6) Drawback :
I didn't run any test with naoqi proxy like ALFaceDetection but there is a high chance that it will conflict with the camera buffer due to naoqi-service accessing the device at the same time with gstreamer.
But for people like me interested in image processing and SLAM approach it makes a huge difference between a 10fps QVGA and a 24fps VGA.



7) TODO and issue :
a) Stream depth image :

I didn't managed to take control of the ASUS Xtion device on Pepper to get the depth stream, I couldn't compile openni2+primesense driver on openvirtual nao VM and I didn't figure how aldebaran is accessing the device because there is no openni library on the Pepper. Here is the informations I gathered :
- ASUS Xtion is located on usb bus 1 device 5 :
Pepper [0] ~ $ lsusb
Bus 001 Device 007: ID 0cf3:9374 Atheros Communications, Inc.
Bus 001 Device 005: ID 1d27:0601 ASUS
Bus 001 Device 010: ID 18d1:deee Google Inc.
Bus 001 Device 006: ID ffff:0006  
Bus 001 Device 004: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
Bus 001 Device 003: ID 0000:0000  
Bus 001 Device 002: ID 8087:07e6 Intel Corp.
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

- ASUS Xtion is accessible at /dev/bus/usb/001/005
Pepper [0] ~ $ lsof|grep usb
2990    /opt/aldebaran/bin/hal    /dev/bus/usb/001/006
3095    /opt/aldebaran/bin/naoqi-service    /dev/bus/usb/001/005
3412    /opt/aldebaran/share/naoqi/applauncher/adb    /dev/bus/usb/001/010


b) depth_registered drop to 3fps

rgbd_launch is in charge of the computation of image_rect and depth registration. For now I didn't figure why depth_registered drop to 3fps and no point cloud is published. This seems to be related with the clocks and queue_size (timestamp coming from gstreamer may conflict or queue_size is not large enough to match RGB with depth frame). And this seems to create a cpu overload of the nodelet :
https://gm1.ggpht.com/sR72gYEqd9j1G2HD5F2lh_fJaT0zCavY67-YqLQTAZH_0IAqLPyWdyqQMsVSV_vif7Nj-faFraVWKDjLO16FBnsTGpYxiMaVBPI9AtqkqfOgGf8QVS_NJCgp7FUOl_0PELeDx9cXxdJq8YGizcGJerC-aCEo-oq6avJYGgXNc05NXpqNF42SkJ4AMpy9KShNrSiscDwXTO-kN5_qophAHWu5FPj51cuQl6rawKzpeGDIuE2OVrw1GDpvHAh_fc4pCBUssK1YaCbGVKOgN5crYiNGZhtWXOqrtibTKFD8_yerYEUSIh-2uaK0H-muOO3w_UaD7hQhgTluJzTOsVcEYNtpiimOJQI7UMmz5VNFcWMt_XE0OKtI-7U69C__I80DKYTIdtOJprjjG669eoXsV9-f7kvTyjPEyV8BImttpNYmdGo9gum2uTg7Z7QlfGmyJoYkVThn99w81tcDAij7oJ7iIspAvHaDYVZZvKvIOwOGpH-hJbM_DMsqjjoKOj8mFhJwb9-KXgYoD1L7843m1epRfcmFuSTHDvdk8HgEWt4NMP3-NgbP8aSfBTzsT6UDvzCTqkQv3G7Q3iAnI6ghvE54faWWQB1Y4XzIW9JlmZOALbfOVgZagwL9kxzQtqh71q6wwKXuEmJyVNLYvpidJBKE98xrLCJ5Fwh1OyrZCWXoJeJoRptMp8qKAryiggvLx3yQjPpCucatihpyvMFnO-Fqs5PY=w1136-h174-l75-ft

Note that I'm running on a i7 and 32Go of RAM, the machine is overpowered for this application so there must be a configuration issue for the depth registration.

If anyone finds a way to solve the depth registration issue or/and to get the control on the ASUS Xtion let me know !

Thanks.






You have to understand that the word "service" actually means two different things in NAOqi. See an explanation here:

    NAOqi services (also called "modules"), that expose an API and are registered to the ServiceDirectory. You can call them with qicli, subscribe to their signals, etc.

    systemd services, that are standalone executables packaged in an Application Package, declared in it's manifest with a tag. These are managed by ALServiceManager, who can start and stop them (they will have their own process). For clarity's sake, these are called "Executables" in this doc.

    The confusion between the two is increased by the fact that a common pattern is to write an executable whose sole purpose is to run a NAOqi service, and sometimes to identify both with the same name (e.g. both are called “ALFuchsiaBallTracker”).

Your problem here is that the NAOqi service ALTactileGesture is run by the executable registered under the ID ALTactileGesture-serv. So you need to do

ALServiceManager.stop("ALTactileGesture-serv")

(I just tested it, it works fine)

(edit) by the way, I'm not sure that actually stopping and starting ALTactileGesture is the best way of doing what you're trying to do (it seems a bit hacky to me), but if you want to do it that way, this is how :)




