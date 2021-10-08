# synchCams package
# this package starts acquisition of two cameras that alternate in capturing frames
# very important:
# the two cameras if both USB, should be connected to different USB cards (different sides of laptop for instance), otherwise it is not possible to acquire from both cameras.

 
 
 Troubleshooting:
 In case the cameras are not detected (perhaps because of program crash) remove and replug the USB cameras
This problem got solved using some combination of 

in anaconda prompt:
setx OPENCV_VIDEOIO_PRIORITY_MSMF 1
setx OPENCV_VIDEOIO_DEBUG 1

in scrript
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

not sure which exact one but I am not able to reproduce the error.

Note that the setx effects the next time one opens the command prompt not immediately.

There was also an error in which the camera didn't get the right frame rate (was giving as 0.0)

To see the set values in cmd use:
set

usually when video is not saved via videowritor, its usually because the frame size or fps is not correct.

ResolvePackageNotFound error describes all packages not installed yet, but required.
To solve the problem, move them under pip section: