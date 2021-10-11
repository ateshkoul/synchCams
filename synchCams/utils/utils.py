# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:15:30 2020

@author: AKoul
"""
import json
import pdb
import random

def get_current_list(filename):
    # this function is meant to do something tricky-
    # return a counterbalanced order of conditions
    
    # read file
    with open(filename, 'r') as myfile:
        data=myfile.read()
        
    # parse file
    obj = json.loads(data)
    
    
    values = list(obj.items())
    
    random.shuffle(values)
    
    obj = dict(values)
    
#    pdb.set_trace()
    for cur_key,cur_value in obj.items():
        if('min_value' not in locals()):
            min_value = cur_value 
        if cur_value <= min_value:
            min_value = cur_value
            min_key = cur_key
#    print(min_value)
    return min_key
    

def update_list(filename,key):
    with open(filename, 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)
#    pdb.set_trace()
    obj[key] = obj[key] + 1
    with open(filename, 'w') as outfile:
        json.dump(obj, outfile)

#{k: v for k, v in sorted(obj.items(), key=lambda item: item[1])}
#
#min_value = 0
#for cur_key,cur_value in obj.items():
#    if min_value <= cur_value:
#        min_value = cur_value
#        min_key = cur_key

import cv2
import time
import pdb
def approx_frame_rate(device):
    print("Checking camera for frame rate......")
 
    # Start default camera
    video = cv2.VideoCapture(device+ cv2.CAP_DSHOW);
    if not video.read()[0]:
        raise IndexError("Camera index not read! Camera not ready")
     
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.
     
#    if int(major_ver)  < 3 :
#        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
#        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
#    else :
#        fps = video.get(cv2.CAP_PROP_FPS)
#        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
     
 
    # Number of frames to capture
    num_frames = 120;
#    video.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    video.set(cv2.CAP_PROP_FPS, 30)
    
#    print(video.get(cv2.CAP_PROP_FPS))
#          self.cam[str(device)] = cv2.VideoCapture(device+ 
    print("\nCapturing {0} frames".format(num_frames))
 
    # Start time
    start = time.time()
     
    # Grab a few frames
    for i in range(0, num_frames) :
        ret, frame = video.read()
 
     
    # End time
    end = time.time()
 
    # Time elapsed
    seconds = end - start
    print("Time taken : {0} seconds".format(seconds))
 
    # Calculate frames per second
    fps  = num_frames / seconds;
    print("Estimated frames per second : {0}".format(fps));
 
    # Release video
    video.release()
    return fps

def check_webcam(device):
    video = cv2.VideoCapture(device);
    
    # Number of frames to capture
    num_frames = 200;
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (480,50)
    fontScale              = 2
    fontColor              = (0,0,0)
    lineType               = 2
    
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#    pdb.set_trace()
    out= cv2.VideoWriter('Video_test.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1920,1080))
    
    print(video.get(3))
    print(video.get(4))

    for i in range(0, num_frames) :
        ret, frame = video.read()
#        pdb.set_trace()
        cv2.putText(frame,'REC',
                    bottomLeftCornerOfText,
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
#        print(len(frame))
        out.write(frame)
        cv2.imshow("0",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # Release video
    video.release()
    cv2.destroyAllWindows() 

# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False