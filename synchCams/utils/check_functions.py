# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:49:36 2020

@author: AKoul
"""

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
                
#        checking a string is tricky as even 2 can be checked as '2' so not using it 
#        if subject_data_dict['subject_name'] is not str:
#            print("\nsubject_name is not an string")
#            print("\nPlease reenter the value: ")
#            subject_data_dict['session_no'] = input("Enter the subject name ")
#            try:
#                str(subject_data_dict['session_no'])
#                check_flag_subject_name = False 
#            except:
#                check_flag_subject_name = True
#        
#        if subject_data_dict['subject_sex'] is not str:
#            print("\nsubject_sex is not an integer")
#            print("\nPlease reenter the value: ")
#            subject_data_dict['subject_sex'] = input("Enter the subject Sex ")
#            try:
#                str(subject_data_dict['subject_sex'])
#                check_flag_subject_sex = False
#            except:
#                check_flag_subject_sex = False
        
#        if ((subject_data_dict['session_no'] is not int) & check_flag_session_no):
#            print("\nsession_no is not an integer")
#            print("\nPlease reenter the value: ")
#            subject_data_dict['session_no'] = input("Enter the subject session no ")
#            try:
#                subject_data_dict['session_no'] = int(subject_data_dict['session_no'])
#                check_flag_session_no = False
#            except:
#                check_flag_session_no = True
#    pdb.set_trace()
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