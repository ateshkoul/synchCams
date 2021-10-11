# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 17:31:19 2020

@author: AKoul
"""
import cv2
import threading
import time
import pdb
import os
import json
import serial

class camThread_check(threading.Thread):
    def __init__(self, synchCam,device):
        threading.Thread.__init__(self)
#        self.previewName = previewName
        self.synchCam = synchCam
        self.device = device
    def run(self):
        print("Starting Webcam " + str(self.device))
        camPreview(self.synchCam,self.device)

        
def camPreview(synchCam,device):    

    video = synchCam.cam[str(device)]
#    pdb.set_trace()
    # doesn't work
#    video.set(cv2.CAP_PROP_FPS, 30)
#    
#    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    num_frames = 120;

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
#    start_time = time.time()
#    capture_duration = 10
    
#    cv2.namedWindow(previewName)
#    while(int(time.time() - start_time) < capture_duration):
#        
##        pdb.set_trace()
##        if cam.isOpened():  # try to get the first frame
##            rval, frame = cam.read()
##        else:
##            rval = False
#        
#        rval, frame = video.read()
#        cv2.imshow(previewName, frame)
##        key = cv2.waitKey(20)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
        
    print(int(video.get(3)))
    print(int(video.get(4)))
    print("\n\nWebCam is ready!")
       
#    cv2.destroyWindow(previewName)



class camThread_runtask(threading.Thread):
    def __init__(self, synchCam,device,codes,task_name,capture_duration):
        threading.Thread.__init__(self)
        self.device = device
        self.codes = codes
        self.task_name = task_name
        self.capture_duration = capture_duration
        self.results = dict()
        # this is to just check that the webcams are being recongnized
        # and nothing more. the cv2.VideoCapture can't be item assigned 
        # so can't do self.cam[device] = ...
        #pdb.set_trace()
        self.cam = dict()
        self.serial = synchCam.serial

        
        self.cam[str(device)] = synchCam.cam[str(device)]
        self.cam[str(device)+'_frame_width'] = synchCam.cam[str(device)+'_frame_width']
        self.cam[str(device)+'_frame_height'] = synchCam.cam[str(device)+'_frame_height']
        self.cam[str(device)+'_fps'] = synchCam.cam[str(device)+'_fps']
#        
#        pdb.set_trace()
        self.results = synchCam.results
        self.results['cam'+str(device)+'_frame_width'] = synchCam.cam[str(device)+'_frame_width']
        self.results['cam'+str(device)+'_frame_height'] = synchCam.cam[str(device)+'_frame_height']
        
#        self.results['path'] = os.path.join("Data","Sub_%.3d" % self.results['subject_no'],"Ses_%.3d" % self.results['session_no'])
        
        
        
    def run(self):
        print("Starting " + self.task_name)
        start_acq_buffer(self,self.device)


def start_acq_buffer(self,device):
    
    print("Thread started at %s" % (time.ctime(time.time())))
    # this function basically records more camera overall, so that there is a buffer as well 
    # TO DO: add timestamps in json files
    out = dict()
    frames = dict()
    #      capture_duration = 10
    nframes = 0
    buffer_time = 40
    video_frame_rate = self.cam[str(device)+'_fps'] # this has to be changed or gotten from the camera details
  
    print(video_frame_rate)
    if not self.serial.is_open:
        self.serial.open()
#    pdb.set_trace()
    out[str(device)] = cv2.VideoWriter(os.path.join(self.results['path'],'Video_'+str(device)+'_'+self.task_name+'.avi'),cv2.VideoWriter_fourcc('M','J','P','G'), video_frame_rate, (self.cam[str(device)+'_frame_width'],self.cam[str(device)+'_frame_height']))
    
    rotation_matrix=cv2.getRotationMatrix2D((self.cam[str(device)+'_frame_width']/2, self.cam[str(device)+'_frame_height']/2),-90,1)

    
    start_time = time.time()
#      start_trigger = time.time()
#      self.serial.write(chr(codes[0]).encode())
    timestamps = dict()
    while(int(time.time() - start_time) < (self.capture_duration+buffer_time)):
        
        
        # this is a very rough estimate, will depend on frame rate of the cameras
        # but has the good property that it is unique value
        # this ensures that we have initial buffer
               
#          if(nframes ==100):
        # this is very ugly and very ad-hoc. However, for not this should suffice
        # so that the trigger is sent only once and not multiple times
        # plus this way the procedure is the same for start and end trigger
        if('start_trigger' not in locals()):
            if(int(time.time()-start_time) ==30):
                
#               print(int(time.time()-start_time))
               start_trigger = time.time()
               #self.serial.write(chr(codes[0]))
               self.serial.write(chr(self.codes[0]).encode())

        ret, frame = self.cam[str(device)].read()
        timestamps[str(device)+'_timestamp_'+str(nframes)]= time.time()
#        print("Frame captured at %s" % (time.ctime(time.time())))
        
#        rotated_frame=cv2.warpAffine(frame,rotation_matrix,(self.cam[str(device)+'_frame_width'],self.cam[str(device)+'_frame_height']))

        #pdb.set_trace()
#        frames[str(device)] = rotated_frame
        frames[str(device)] = frame


        out[str(device)].write(frames[str(device)])
            #pdb.set_trace()
        cv2.imshow(str(device),frames[str(device)])
#            cv2.imshow("0",frames[str(device)])

            # this is to keep incase something goes wrong
            # doesn't work fully but needs to be kept so that the images are shown 18-02:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.serial.write(chr(self.codes[1]).encode())
            break
        nframes+= 1
#              if(nframes ==cam_frame_rate*capture_duration+100):
#              pdb.set_trace()
            # if the start trigger has been sent
        if(('start_trigger' in locals()) & ('end_trigger' not in locals())):
            # and the time interval is more than 10 seconds, send a trigger
            if(int(time.time()-start_trigger)==self.capture_duration):
                end_trigger = time.time()
#                pdb.set_trace()
                duration_trial = end_trigger - start_trigger
#               #self.serial.write(chr(codes[1]))
                self.serial.write(chr(self.codes[1]).encode())
#                self.cam[str(device)].release()

  # save results:
    self.results['capture_duration'] = self.capture_duration
    self.results['total_frames_captured']= nframes
    self.results['buffer_time'] = buffer_time
    self.results['video_frame_rate'] = video_frame_rate
    # already saved above
#    self.results['cam_frame_rate'] = self.cam[str(self.device)+'_fps']
    self.results['start_time'] = start_time
    self.results['start_trigger'] = start_trigger
    self.results['end_trigger'] = end_trigger
    self.results['duration_trial'] = duration_trial
    self.results['script_name'] = os.path.basename(__file__)
  
    print('saving '+ self.task_name+' data..')
    if os.path.exists(os.path.join(self.results['path'],'result_'+str(device)+"_"+self.task_name+'.json')):
        print("A file already exists!")
        overwrite = input("Do you want to overwrite it? y/n ")
        if overwrite == 'y':
            with open(os.path.join(self.results['path'],'result_'+str(device)+"_"+self.task_name+'.json'), 'w') as outfile:
                json.dump(self.results, outfile)
    else:
        with open(os.path.join(self.results['path'],'result_'+str(device)+"_"+self.task_name+'.json'), 'w') as outfile:
            json.dump(self.results, outfile)
            
    print("Finished the task "+ self.task_name)

    print('saving '+ self.task_name+' timestamp data..')
    if os.path.exists(os.path.join(self.results['path'],'timestamp_'+str(device)+"_"+self.task_name+'.json')):
        print("A file already exists!")
        overwrite = input("Do you want to overwrite it? y/n ")
        if overwrite == 'y':
            with open(os.path.join(self.results['path'],'timestamp_'+str(device)+"_"+self.task_name+'.json'), 'w') as outfile:
                json.dump(timestamps, outfile)
    else:
        with open(os.path.join(self.results['path'],'timestamp_'+str(device)+"_"+self.task_name+'.json'), 'w') as outfile:
            json.dump(timestamps, outfile)
      
    cv2.destroyAllWindows()






