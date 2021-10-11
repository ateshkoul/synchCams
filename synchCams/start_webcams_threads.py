import cv2
#import matplotlib.pyplot as plt
import pdb
import time
import serial
import json
import os
from check_frame_rate import approx_frame_rate
import cam_threads
from utils import get_current_list,update_list

# TO DO:
# Change to 2 min acquisition
# remove baseline1 and baseline 2

# To Do:
# check the synchronousity of the camera acquisition


# condition specific triggers

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

def check_input(input_value,allowed_values):
    check_flag = True
    
    
    while(check_flag):
        if input_value in allowed_values:
            input_value = input_value
            check_flag = False
            print("input value is " + input_value)
        else:
            print("Input value not valid. Please try again")
            input_value = input("Please reenter the value: ")
    return input_value


def check_subject_datatype(subject_data_dict):
    check_flag_subject_no = True
#    check_flag_subject_name = True
#    check_flag_subject_sex = True
    check_flag_session_no = True   
    
#    while(check_flag_subject_no | check_flag_subject_name | check_flag_subject_sex | check_flag_session_no):
    while(check_flag_subject_no | check_flag_session_no):
        
        try:
            # by default the input function takes values as strings
            subject_data_dict['subject_no'] = int(subject_data_dict['subject_no'])
            check_flag_subject_no = False
        except:
            print("\nsubject_no is not an integer")
            print("\nPlease reenter the value: ")
            subject_data_dict['subject_no'] = input("Enter the subject No ")
            check_flag_subject_no = True
        try:
            # by default the input function takes values as strings
            subject_data_dict['session_no'] = int(subject_data_dict['session_no'])
            check_flag_session_no = False
        except:
            print("\nsession_no is not an integer")
            print("\nPlease reenter the value: ")
            subject_data_dict['session_no'] = input("Enter the session no ")
            check_flag_session_no = True   
                
    return subject_data_dict

def check_subject_data(subject_data_dict,proceed,allowed_values=['y','yes','']):
    check_flag = True
    
    
    while(check_flag):
        if proceed in allowed_values:
            subject_data_dict = check_subject_datatype(subject_data_dict)
#            subject_data_dict = subject_data_dict
            check_flag = False
            print("\nValues entered: \n"+ 
                            "\nsubject_no:" + str(subject_data_dict['subject_no']) +
                            "\nsubject_name:" + str(subject_data_dict['subject_name']) +
                            "\nsubject_sex:" + str(subject_data_dict['subject_sex']) +
                            "\nsession_no:" + str(subject_data_dict['session_no'])+ "\n")
        else:
            print("\nPlease reenter the values: ")
            subject_data_dict['subject_no'] = input("Enter the subject No ")
            subject_data_dict['subject_name'] = input("Enter the subject Name ")
            subject_data_dict['subject_sex'] = input("Enter the subject Sex ")
            subject_data_dict['session_no'] = input("Enter the subject session no ")
            subject_data_dict = check_subject_datatype(subject_data_dict)
            proceed = input("\nProceed with these values? y/n \n"+ 
                            "subject_no: " + str(subject_data_dict['subject_no']) +
                            "\nsubject_name: " + str(subject_data_dict['subject_name']) +
                            "\nsubject_sex: " + str(subject_data_dict['subject_sex']) +
                            "\nsession_no: " + str(subject_data_dict['session_no']) + "\n")
            
    return subject_data_dict




        
        
        


class synchCam():
#  def __init__(self,device_nos,portname='/dev/ttyUSB0'):
#  def __init__(self,device_nos,portname='COM4'):
  def __init__(self,device_nos,portname='COM3'):

      self.results = dict()
      # this is to just check that the webcams are being recongnized
      # and nothing more. the cv2.VideoCapture can't be item assigned 
      # so can't do self.cam[device] = ...
      #pdb.set_trace()
      self.cam = dict()
      self.devices = device_nos
      self.serial = serial.Serial(port = portname,baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, rtscts=False)
      print("Serial port opened!")
      self.serial.write(chr(250).encode())
      print("\nChecking Webcams started....")
      
#      cam_thread_check_1 = cam_threads.camThread_check("Camera 1", 0)
#      cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
#      cam_thread_check_1.start()
#      cam_thread_check_2.start()
#      pdb.set_trace()
      
      
#      fps_devices = [32,30]
      
      for device in device_nos:
          self.cam[str(device)] = cv2.VideoCapture(device)
          
          self.cam[str(device)].set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
          self.cam[str(device)].set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
          self.cam[str(device)].set(cv2.CAP_PROP_FPS, 30)
#        self.cam[str(device)+'_fps'] = self.cam[str(device)].get(cv2.CAP_PROP_FPS)
        
          self.cam[str(device)+'_frame_width'] = int(self.cam[str(device)].get(3))
          self.cam[str(device)+'_frame_height'] = int(self.cam[str(device)].get(4))
          
          self.cam[str(device)+'_fps'] = self.cam[str(device)].get(cv2.CAP_PROP_FPS)
#          self.cam[str(device)+'_fps'] = fps_devices[device]
          

#      cam_thread_check_device_1 = cam_threads.camThread_check(self,device)
##          cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
#      cam_thread_check_device_1.start()
#      
#      cam_thread_check_device_2 = cam_threads.camThread_check(self,device)
##          cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
#      cam_thread_check_device_2.start()
#      
#      cam_thread_check_device_1.join()
#      cam_thread_check_device_2.join()
#      
#          
#      pdb.set_trace()
          
      cam_thread_check_device = dict()
      for device in device_nos:
#          # this function has to be above because otherwise the camera is not released
#          # this leads to the image in the camera being 0
#          # this operation is necessary because for some reason, the cv2.CAP_PROP_FPS property
#          # provides a 0.0 fps
#          self.cam[str(device)+'_fps'] = approx_frame_rate(device)
          cam_thread_check_device[str(device)] = cam_threads.camThread_check(self,device)
#          cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
#      for device in device_nos:
          cam_thread_check_device[str(device)].start()
      
      for device in device_nos:
          cam_thread_check_device[str(device)].join()
        
        
        
#      pdb.set_trace()
      
#      for device in device_nos:
##          # this function has to be above because otherwise the camera is not released
##          # this leads to the image in the camera being 0
##          # this operation is necessary because for some reason, the cv2.CAP_PROP_FPS property
##          # provides a 0.0 fps
##          self.cam[str(device)+'_fps'] = approx_frame_rate(device)
#          cam_thread_check_device = cam_threads.camThread_check(str(device), device)
##          cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
#          cam_thread_check_device.start()
#    
#          
#
#          self.cam[str(device)] = cv2.VideoCapture(device)
#          
#          # have to set both of them for the laptop to be able to change the resolution
#          # this problem doesn't occur for the desktop
##          self.cam[str(device)].set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
##          self.cam[str(device)].set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
##          self.cam[str(device)].set(cv2.CAP_PROP_FPS, 30)
#          print(self.cam[str(device)].get(cv2.CAP_PROP_FPS))
##          self.cam[str(device)] = cv2.VideoCapture(device+ cv2.CAP_DSHOW)  # camera index (default = 0) (added based on Randyr's comment).
##          pdb.set_trace()
##          self.cam[str(device)].set(3,160)
##          self.cam[str(device)].set(4,120)
#          print('cam has image : %s' % self.cam[str(device)].read()[0]) # True = got image captured. 
#                                               # False = no pics for you to shoot at.
#
#          
#          if not self.cam[str(device)].read()[0]:
#              raise IndexError("Camera index not read! Camera not ready")
#              
##          pdb.set_trace()
#          self.cam[str(device)+'_frame_width'] = int(self.cam[str(device)].get(3))
#          self.cam[str(device)+'_frame_height'] = int(self.cam[str(device)].get(4))
#          self.results['cam'+str(device)+'_frame_width'] = self.cam[str(device)+'_frame_width']
#          self.results['cam'+str(device)+'_frame_height'] = self.cam[str(device)+'_frame_height']
          
#          self.cam[str(device)].release()
    
      
      
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
#      self.results['path'] = os.path.join("Data","Sub_" + str(self.results['subject_no']),"Ses_" + str(self.results['session_no']))
#      pdb.set_trace()
      self.results['path'] = os.path.join("Data","Sub_%.3d" % self.results['subject_no'],"Ses_%.3d" % self.results['session_no'])
#      pdb.set_trace()
      try:
          if not os.path.exists(self.results['path']):
              # create a path if it doesn't exist
              os.makedirs(self.results['path'])
      except OSError:
          print ("Creation of the directory %s failed" % self.results['path'])
      else:
          print ("Successfully created the directory %s " % self.results['path'])
      

  def run_task_buffer(self,task_name,capture_duration = 120):
    #pdb.set_trace()
    sleep_time = 2
    for case in switch(task_name):
        if case('baseline1'):
            # in theory the two commands could be combined but 
            # I want to keep the check_input function as general as possible
            # I would loose the specific condition names
            acquisition = input("Start the baseline1? y/n ")
            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
            

#            pdb.set_trace()
            if acquisition in ['y', 'yes']:
                cam_thread_run_task = dict()
                for device in self.devices:
                    cam_thread_run_task['device'] = cam_threads.camThread_runtask(synchCam = self,device=device,codes = (10,11),task_name=task_name,capture_duration=capture_duration)
#                   cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
                    cam_thread_run_task['device'].start()
                    
                # wait till all the threads are finished 
                for device in self.devices:
                    cam_thread_run_task['device'].join()
                time.sleep(sleep_time)
            break
        if case('FaOcc'):
            acquisition = input("Start the Far with Occluder?  y/n ")
            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])

            if acquisition in ['y', 'yes']:
                cam_thread_run_task = dict()
                for device in self.devices:
                    cam_thread_run_task['device'] = cam_threads.camThread_runtask(synchCam = self,device=device,codes = (20,21),task_name=task_name,capture_duration=capture_duration)
#                   cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
                    cam_thread_run_task['device'].start()
                    
                # wait till all the threads are finished 
                for device in self.devices:
                    cam_thread_run_task['device'].join()               
                time.sleep(sleep_time)
#                self.start_acq_buffer(codes = (20,21),task_name=task_name,capture_duration=capture_duration)
            break
        if case('FaNoOcc'):
            acquisition = input("Start the Far with No Occluder?  y/n ")
            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])

            if acquisition in ['y', 'yes']:
                cam_thread_run_task = dict()
                for device in self.devices:
                    cam_thread_run_task['device'] = cam_threads.camThread_runtask(synchCam = self,device=device,codes = (30,31),task_name=task_name,capture_duration=capture_duration)
#                   cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
                    cam_thread_run_task['device'].start()
                    
                # wait till all the threads are finished 
                for device in self.devices:
                    cam_thread_run_task['device'].join()
                time.sleep(sleep_time)
            break
        if case('NeOcc'):
            acquisition = input("Start the Near with Occluder?  y/n ")
            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
            if acquisition in ['y', 'yes']:
                cam_thread_run_task = dict()
                for device in self.devices:
                    cam_thread_run_task['device'] = cam_threads.camThread_runtask(synchCam = self,device=device,codes = (40,41),task_name=task_name,capture_duration=capture_duration)
#                   cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
                    cam_thread_run_task['device'].start()
                    
                # wait till all the threads are finished 
                for device in self.devices:
                    cam_thread_run_task['device'].join()
                time.sleep(sleep_time)
            break
        if case('NeNoOcc'):
            acquisition = input("Start the Near with No Occluder?  y/n ")
            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
            if acquisition in ['y', 'yes']:
                cam_thread_run_task = dict()
                for device in self.devices:
                    cam_thread_run_task['device'] = cam_threads.camThread_runtask(synchCam = self,device=device,codes = (50,51),task_name=task_name,capture_duration=capture_duration)
#                   cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
                    cam_thread_run_task['device'].start()
                    
                # wait till all the threads are finished 
                for device in self.devices:
                    cam_thread_run_task['device'].join()
                time.sleep(sleep_time)
            break
        if case('baseline2'):
            acquisition = input("Start the baseline2 acquisition?  y/n ")
            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
            if acquisition in ['y', 'yes']:
                cam_thread_run_task = dict()
                for device in self.devices:
                    cam_thread_run_task['device'] = cam_threads.camThread_runtask(synchCam = self,device=device,codes = (60,61),task_name=task_name,capture_duration=capture_duration)
#                   cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
                    cam_thread_run_task['device'].start()
                    
                # wait till all the threads are finished 
                for device in self.devices:
                    cam_thread_run_task['device'].join()
                time.sleep(sleep_time)
            break
        if case('test'):
            capture_duration = 20
            acquisition = input("Start the test acquisition?  y/n ")
            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
            if acquisition in ['y', 'yes']:
                

#                cam_thread_run_task_1 = cam_threads.camThread_runtask(self_var = self,device_no=0,codes = (70,71),task_name=task_name,capture_duration=capture_duration)
#                cam_thread_run_task_1.start()
#                
#                
#                cam_thread_run_task_2 = cam_threads.camThread_runtask(self_var = self,device_no=1,codes = (70,71),task_name=task_name,capture_duration=capture_duration)
#                cam_thread_run_task_2.start()
#                for device in self.devices:
#                    cam_thread_run_task = cam_threads.camThread_runtask(synchCam = self,device=device,codes = (70,71),task_name=task_name,capture_duration=capture_duration)
##                   cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
#                    cam_thread_run_task.start()                
                
                cam_thread_run_task = dict()
                for device in self.devices:
                    cam_thread_run_task['device'] = cam_threads.camThread_runtask(synchCam = self,device=device,codes = (70,71),task_name=task_name,capture_duration=capture_duration)
#                   cam_thread_check_2 = cam_threads.camThread_check("Camera 2", 1)
                    cam_thread_run_task['device'].start()
                    
                # wait till all the threads are finished 
                for device in self.devices:
                    cam_thread_run_task['device'].join()
                time.sleep(sleep_time)
                    
#                proceed = input("Proceed? y/n ")
#                proceed = check_input(input_value=proceed,allowed_values=['y','yes','n','no'])
            break
                
        if case(): # default, could also just omit condition or 'if True'
            print("something else!")
            # No need to break here, it'll stop anyway 
            

  def start_experiment(self):
      task_list = ['FaOcc','FaNoOcc','NeOcc','NeNoOcc']
      
      # not randomized for now
#      randomized_task_list = task_list
      

      randomized_order_key = get_current_list('condition_sequence.json')
#      print(randomized_order_key)
      randomized_order = eval(randomized_order_key.split()[0])
      randomized_task_list = [ task_list[i] for i in randomized_order]
      update_list('condition_sequence.json',randomized_order_key)
#      pdb.set_trace()
      # for the monkey experiment only the 4 conditions
#      final_task_list = ['test','baseline1'] + randomized_task_list + ['baseline2']
      final_task_list = ['test'] + randomized_task_list
      print("The experimental conditions are :" + " ".join(randomized_task_list))
      self.results['final_task_list'] = final_task_list
      proceed = input("To proceed press enter ")
      
      if not proceed:
          for task_name in final_task_list:
              self.run_task_buffer(task_name)
#          self.results['final_task_list'] = final_task_list
      else:
          print("You pressed " + proceed)
          confirm_proceed = input(" Do you want to stop experiment? y/n ")
          if confirm_proceed == 'n':
              for task_name in final_task_list:
                  self.run_task_buffer(task_name)
#              self.results['final_task_list'] = final_task_list     

#  def start_experiment(self):
#      task_list = ['FaOcc','FaNoOcc','NeOcc','NeNoOcc']
#      # not randomized for now
#      randomized_task_list = task_list
#      # for the monkey experiment only the 4 conditions
##      final_task_list = ['test','baseline1'] + randomized_task_list + ['baseline2']
#      final_task_list = ['test'] + randomized_task_list
#      print("The experimental conditions are :" + " ".join(task_list))
#      
#      proceed = input("To proceed press enter ")
#      
#      if not proceed:
#          for task_name in final_task_list:
#              self.run_task_buffer(task_name)
#          self.results['final_task_list'] = final_task_list
#      else:
#          print("You pressed " + proceed)
#          confirm_proceed = input(" Do you want to stop experiment? y/n ")
#          if confirm_proceed == 'n':
#              for task_name in final_task_list:
#                  self.run_task_buffer(task_name)
#              self.results['final_task_list'] = final_task_list     
      
  
  def releaseCams(self):
      for device in self.devices:
          print("releasing cameras")
          self.cam[str(device)].release()
          
      

if __name__ == "__main__":
#    os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
    rec = synchCam([0,1])
#    time.sleep(10)
	
    print("Experiment starting..")
    rec.subject_data()
    rec.start_experiment()
    rec.releaseCams()
    rec.serial.close()
