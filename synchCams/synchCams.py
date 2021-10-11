# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:47:37 2020

@author: Iannettilab
"""

import cv2
import serial
from synchCams.utils.check_functions import check_subject_data,check_input
from synchCams.utils.utils import approx_frame_rate,switch,get_current_list,update_list
import os
import pdb
import time
import json
    
class synchCams():
  def __init__(self,device_nos,portname='COM1'):

      self.results = dict()
      # this is to just check that the webcams are being recongnized
      # and nothing more. the cv2.VideoCapture can't be item assigned 
      # so can't do self.cam[device] = ...
      #pdb.set_trace()
      self.cam = dict()
      self.devices = device_nos
      # this is config for receiving from biosemi
#      self.serial = serial.Serial(port = portname,baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, rtscts=False)
      self.serial = serial.Serial(port = portname)

      
      print("\nChecking Webcams started....")
      for device in device_nos:
          # this function has to be above because otherwise the camera is not released
          # this leads to the image in the camera being 0
          # this operation is necessary because for some reason, the cv2.CAP_PROP_FPS property
          # provides a 0.0 fps
          self.cam[str(device)+'_fps'] = approx_frame_rate(device)
          # self.cam[str(device)+'_fps'] = 15

          self.cam[str(device)] = cv2.VideoCapture(device+ cv2.CAP_DSHOW)
#          self.cam[str(device)].set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
          # have to set both of them for the laptop to be able to change the resolution
          # this problem doesn't occur for the desktop
          self.cam[str(device)].set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
          self.cam[str(device)].set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
          self.cam[str(device)].set(cv2.CAP_PROP_FPS, 30)
#          self.cam[str(device)] = cv2.VideoCapture(device+ cv2.CAP_DSHOW)  # camera index (default = 0) (added based on Randyr's comment).
          print('cam has image : %s' % self.cam[str(device)].read()[0]) # True = got image captured. 
                                               # False = no pics for you to shoot at.

          
          if not self.cam[str(device)].read()[0]:
              raise IndexError("Camera index not read! Camera not ready")
              
#          pdb.set_trace()
          self.cam[str(device)+'_frame_width'] = int(self.cam[str(device)].get(3))
          self.cam[str(device)+'_frame_height'] = int(self.cam[str(device)].get(4))
          self.results['cam'+str(device)+'_frame_width'] = self.cam[str(device)+'_frame_width']
          self.results['cam'+str(device)+'_frame_height'] = self.cam[str(device)+'_frame_height']
          
#          self.cam[str(device)].release()
    
      print("\n\nWebCams are ready!")
      # print("Serial port opened!")
      # self.serial.read()
  
  def create_sub_dir(self,sub_entry):
      self.results = sub_entry

      self.results['path'] = os.path.join("Data","Sub_" + str(self.results['subject_no']),"Ses_" + str(self.results['session_no']))

      try:
          if not os.path.exists(self.results['path']):
              # create a path if it doesn't exist
              os.makedirs(self.results['path'])
      except OSError:
          print ("Creation of the directory %s failed" % self.results['path'])
      else:
          print ("Successfully created the directory %s " % self.results['path'])
          
  def subject_data(self):
       print("\nEnter Subject data (press Enter after each information): \n")
       try:
           self.results['subject_no'] = input("Enter the subject No ")
       except:
           print("\nPlease enter a valid integer value")
       self.results['subject_name'] = input("Enter the subject Name ")
       self.results['subject_sex'] = input("Enter the subject Sex ")
       self.results['session_no'] = input("Enter the subject session no ")
       # this is for string in python 2
     #      self.results['subject_no'] = raw_input("Enter the subject No.")
       # create directories for subject data
       proceed = input("\nYou inputted these values. Proceed with them? y/n \n"+ 
                             "\nsubject_no: " + str(self.results['subject_no']) +
                             "\nsubject_name: " + str(self.results['subject_name']) +
                             "\nsubject_sex: " + str(self.results['subject_sex']) +
                             "\nsession_no: " + str(self.results['session_no'])+ "\n")
       self.results = check_subject_data(self.results,proceed)
    
       self.results['path'] = os.path.join("Data","Sub_%.3d" % self.results['subject_no'],"Ses_%.3d" % self.results['session_no'])
       try:
           if not os.path.exists(self.results['path']):
               # create a path if it doesn't exist
               os.makedirs(self.results['path'])
       except OSError:
           print ("Creation of the directory %s failed" % self.results['path'])
       else:
           print ("Successfully created the directory %s " % self.results['path'])
  

  def start_acq_buffer(self,codes,task_name,capture_duration = 120):

      out = dict()
      frames = dict()
      #      capture_duration = 10
      nframes = 0
      buffer_time = 0
      video_frame_rate = 30 # this has to be changed or gotten from the camera details
      
      if not self.serial.is_open:
          self.serial.open()

          
      for device in self.devices:
          # Define the codec and create VideoWriter object.
          out[str(device)] = cv2.VideoWriter(os.path.join(self.results['path'],'Video_'+str(device)+'_'+task_name+'.avi'),cv2.VideoWriter_fourcc('M','J','P','G'), video_frame_rate, (self.cam[str(device)+'_frame_width'],self.cam[str(device)+'_frame_height']))

          self.results['cam'+str(device)+'_fps'] = self.cam[str(device)+'_fps']
        
      start_time = time.time()

      timestamps = dict()
      

      while(int(time.time() - start_time) < (capture_duration+buffer_time)):
          if('start_trigger' not in locals()):
              if(int(time.time()-start_time) ==0):
                  start_trigger = time.time()
                  # for triggering with serial port
#                  self.serial.read()

          for device in self.devices:
              ret, frame = self.cam[str(device)].read()
              timestamps[str(device)+'_timestamp_'+str(nframes)]= time.time()
              
              frames[str(device)] = frame

              out[str(device)].write(frames[str(device)])
              cv2.imshow(str(device),frames[str(device)])   

              if cv2.waitKey(1) & 0xFF == ord('q'):
                  # pdb.set_trace()
                  # in case serial codes are written
                  self.serial.write(chr(codes[1]).encode())
                  #self.serial.close()
                  break
              nframes+= 1
              # if the start trigger has been sent
              if(('start_trigger' in locals()) & ('end_trigger' not in locals())):
                  # and the time interval is more than 10 seconds, send a trigger
                  if(int(time.time()-start_trigger)==capture_duration):
                      end_trigger = time.time()
#                     pdb.set_trace()
                      duration_trial = end_trigger - start_trigger
                      # pdb.set_trace()
#                     #self.serial.write(chr(codes[1]))
                      self.serial.write(chr(codes[1]).encode())
#                     self.cam[str(device)].release()

      # save results:
      self.results['capture_duration'] = capture_duration
      self.results['total_frames_captured']= nframes
      self.results['buffer_time'] = buffer_time
      # already saved above
      self.results['video_frame_rate'] = video_frame_rate
      self.results['start_time'] = start_time
      self.results['start_trigger'] = start_trigger
      self.results['end_trigger'] = end_trigger
      self.results['duration_trial'] = duration_trial
      self.results['script_name'] = os.path.basename(__file__)
      
      print('saving '+ task_name+' data..')
      if os.path.exists(os.path.join(self.results['path'],'result_'+task_name+'.json')):
          print("A file already exists!")
          overwrite = input("Do you want to overwrite it? y/n ")
          if overwrite == 'y':
              with open(os.path.join(self.results['path'],'result_'+task_name+'.json'), 'w') as outfile:
                  json.dump(self.results, outfile)
      else:
          with open(os.path.join(self.results['path'],'result_'+task_name+'.json'), 'w') as outfile:
              json.dump(self.results, outfile)
              
      print('saving '+ task_name+' timestamp data..')
      if os.path.exists(os.path.join(self.results['path'],'timestamp_'+task_name+'.json')):
          print("A file already exists!")
          overwrite = input("Do you want to overwrite it? y/n ")
          if overwrite == 'y':
              with open(os.path.join(self.results['path'],'timestamp_'+task_name+'.json'), 'w') as outfile:
                  json.dump(timestamps, outfile)
      else:
          with open(os.path.join(self.results['path'],'timestamp_'+task_name+'.json'), 'w') as outfile:
              json.dump(timestamps, outfile)
          
      cv2.destroyAllWindows()  
      
  def run_task_buffer(self,task_name,capture_duration = 120):
      
      acquisition = input("Start the Task "+ task_name +  "? y/n ")
      acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
      for case in switch(task_name):
          if case('a'):
              if acquisition in ['y', 'yes']:
                  self.start_acq_buffer(codes = (10,11),task_name=task_name,capture_duration=capture_duration)              
              break
          if case('b'):
              if acquisition in ['y', 'yes']:
                  self.start_acq_buffer(codes = (20,21),task_name=task_name,capture_duration=capture_duration)
              break
          if case('c'):
              if acquisition in ['y', 'yes']:           
                  self.start_acq_buffer(codes = (30,31),task_name=task_name,capture_duration=capture_duration)
              break
          if case('d'):
              if acquisition in ['y', 'yes']:            
                  self.start_acq_buffer(codes = (40,41),task_name=task_name,capture_duration=capture_duration)
              break
          if case(): # default, could also just omit condition or 'if True'
              print("something else!")
            # No need to break here, it'll stop anyway 
            

  def start_experiment(self):
      self.subject_data()
      # 4 example conditions
      task_list = ['a','b','c','d']
      
      cwd = os.path.dirname(os.path.abspath(__file__)) 
#      pdb.set_trace()
      randomized_order_key = get_current_list(cwd+'\\example_condition_sequence.json')
      randomized_order = eval(randomized_order_key.split()[0])
      randomized_task_list = [ task_list[i] for i in randomized_order]
      update_list(cwd+'\\example_condition_sequence.json',randomized_order_key)

      print("The experimental conditions are :" + " ".join(randomized_task_list))
      self.results['final_task_list'] = randomized_task_list
      proceed = input("To proceed press enter ")
      
      if not proceed:
          for task_name in randomized_task_list:
              self.run_task_buffer(task_name)
      else:
          print("You pressed " + proceed)
          confirm_proceed = input(" Do you want to stop experiment? y/n ")
          if confirm_proceed == 'n':
              for task_name in randomized_task_list:
                  self.run_task_buffer(task_name)
     
  
  def releaseCams(self):
      for device in self.devices:
          print("releasing cameras")
          self.cam[str(device)].release()