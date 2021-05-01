# -*- coding: utf-8 -*-
from . import helpers
from . import mailer_utils
import csv
import os
import json
import cv2
import getpass
from datetime import datetime
import time
from collections import namedtuple
from functools import partial


__all__ = ['CsvDataIterator', 'create_certificate','create_n_mail_certificates']


class CsvDataIterator:
    def __init__(self, f_name):
        self.csv_file_name = f_name
    
    def __iter__(self):
        return self.CsvIterator(self.csv_file_name)


    class CsvIterator:
        def __init__(self, f_name):
            self.csv_file_name = f_name
            self.num_data = 0
            try:
                with open(self.csv_file_name) as f:
                    csv_reader = csv.reader(f)
                    self.csv_header = next(csv_reader)
                    self.csv_header = list(map(lambda x:x.strip().lower().replace(' ','_'),self.csv_header))
                    if not self.is_header_valid():
                        self.csv_header = None
                        raise Exception("Invalid Header!!!")
                    self.csv_data = list(csv_reader)
                self.data_length = len(self.csv_data)
                print('Data Length:',self.data_length)
                if self.data_length <= 0:
                    # There no data only header
                    print("There is no data in the file!!!")
                    raise Exception("There is no data in the file!!!")
            except FileNotFoundError as e:
                print(f"Data file \"{self.csv_file_name}\" not found")
                raise e
            except :
                raise
            
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.num_data >= self.data_length:
                raise StopIteration
            else:
                data = self.csv_data[self.num_data]
                self.num_data += 1
                return data

        def is_header_valid(self):
            
            if ('name' in self.csv_header) and ('score' in self.csv_header) and ('email' in self.csv_header):
                return True
            else:
                print()
                print(f'Header: {self.csv_header} is invalid.')
                print('Header for csv file is must.')
                print('Header must have fields \'name\',\'score\' and \'email\'. Lower, upper or mixed case is allowed.')
                print('Please refer to README.md for more details on allowed Header format.')
                return False


@helpers.log_decorator('certificate_mailer.log')
def create_certificate(student_name,course_name,sign_name,certi_template = None,certi_path='.certificates',overwrite=False):
    # test if certificate directory exists. If no create one
    try:
        if certi_template == None: 
            certi_template= os.path.join(os.path.dirname(__file__), 'data/certi_template.jpg')

        if not os.path.exists(certi_path):
            print(f'{certi_path} doesn\'t exist... Creating it...')
            os.mkdir(certi_path)


        certificate_name = '_'.join(f'{course_name}_{student_name}_{sign_name}.jpg'.split())
        certificate_path = os.path.join(certi_path,certificate_name)

        # test if certificate for given student,course name, sign exist 
        # if exists and overwriting is prohibited simply go back
        if (not overwrite) and (os.path.exists(certificate_path)):
            print(f'Certificate {certificate_name} already exists!!! Not creating new....')
            return certificate_path

        #print(certi_template)
        certi_img = cv2.imread(certi_template)

        # load field coordinates
        # Field coordinates are contained json file with name
        # same as template image file
        template_fields_file = '.'.join(certi_template.split('.')[:-1] + ['json'])
        with open(template_fields_file,"r") as f:
            field_coords = json.load(f)

        print(field_coords)            

        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        # Black color in BGR
        color = (0, 0, 0)
        
        y_offset = 5

        # Write Course name

        # We need to put the text at exact center 
        course_name_x_start = field_coords["course_name_start"][0]
        course_name_x_end = field_coords["course_name_end"][0]
        course_name_y = field_coords["course_name_start"][1]
        course_name_scale = 1
        course_name_thickness = 1

        # first calculate height and width of the text
        (txt_width,_),_ = cv2.getTextSize(course_name,font,course_name_scale,course_name_thickness)
    
        course_name_coords = (int(course_name_x_start +((course_name_x_end-course_name_x_start)/2 - txt_width/2)),course_name_y - y_offset)
    
        certi_img = cv2.putText(certi_img, course_name, course_name_coords, font,course_name_scale, color, course_name_thickness, cv2.LINE_AA)
        
        # Write Student name
        
        student_name_x_start = field_coords["student_name_start"][0]
        student_name_x_end = field_coords["student_name_end"][0]
        student_name_y = field_coords["student_name_start"][1]
        student_name_scale = 1.5
        student_name_thickness = 1

        # first calculate height and width of the text
        (txt_width,_),_ = cv2.getTextSize(student_name,font,student_name_scale,student_name_thickness)
        # calculate text coordinates to align text center with field center
        student_name_coords = (int(student_name_x_start +((student_name_x_end-student_name_x_start)/2 - txt_width/2)),student_name_y - y_offset)
        certi_img = cv2.putText(certi_img, student_name, student_name_coords, font,student_name_scale, color, student_name_thickness, cv2.LINE_AA)
        

        # Write Date    
        date_text = datetime.now().strftime("%d %B %Y")
        
        # We need to put the text at exact center 

        date_text_x_start = field_coords["date_start"][0]
        date_text_x_end = field_coords["date_end"][0]
        date_text_y = field_coords["date_start"][1]
        date_text_scale = 0.75
        date_text_thickness = 1

        # first calculate height and width of the text
        (txt_width,_),_ = cv2.getTextSize(date_text,font,date_text_scale,date_text_thickness)
        # calculate text coordinates to align text center with field center
        date_text_coords = (int(date_text_x_start +((date_text_x_end-date_text_x_start)/2 - txt_width/2)),date_text_y - y_offset)
        # Write text into image
        certi_img = cv2.putText(certi_img, date_text, date_text_coords, font,date_text_scale, color, date_text_thickness, cv2.LINE_AA)
        
        # Write Sign name
       
        sign_name_x_start = field_coords["sign_start"][0]
        sign_name_x_end = field_coords["sign_start"][0]
        sign_name_y = field_coords["sign_end"][1]
        sign_name_scale = 1
        sign_name_thickness = 1

        # first calculate height and width of the text
        (txt_width,_),_ = cv2.getTextSize(sign_name,font,sign_name_scale,sign_name_thickness)
        sign_name_coords = (int(sign_name_x_start +((sign_name_x_end-sign_name_x_start)/2 - txt_width/2)),sign_name_y - y_offset)
        certi_img = cv2.putText(certi_img, sign_name, sign_name_coords, font,sign_name_scale, color, sign_name_thickness, cv2.LINE_AA)

        print('done')
        cv2.imwrite(certificate_path,certi_img)
        return certificate_path
    except:
        print(f"Failed To create Certificate for {student_name}")
        raise Exception(f"Failed To create Certificate for {student_name}")



def _map_func_create_n_mail_certi(xx,tuple_type,course_name,sign_name,total_marks,certi_template,
        sender_email,sender_password,mail_interval,certi_path,overwrite,create_certi_only,verbose=False):
    try:
        if len(xx) != 0:
            xx[0] = xx[0].title()
            student = tuple_type(*map(lambda x:x.strip(),xx))
            print('-'*30)
            print(f'Student: Name:{student.name}\t Score:{student.score}\tEmail:{student.email}')
            
            certificate_path = create_certificate(student_name = student.name, course_name = course_name,
                                sign_name = sign_name,certi_template=certi_template,
                                certi_path=certi_path,overwrite=overwrite)
            print(f'Generated certificate: {certificate_path}')

            if not create_certi_only:
                mail_the_certificate(student_name=student.name,student_score=student.score,course_name=course_name,
                        total_marks=total_marks,sign_name=sign_name,certificate_path=certificate_path,
                        receiver_email=student.email,sender_email=sender_email,password=sender_password,verbose=verbose)
                time.sleep(mail_interval)
    except :
        raise

@helpers.internet_check_decorator()
@helpers.log_decorator('certificate_mailer.log')
def mail_the_certificate(student_name,student_score,course_name,total_marks,sign_name,certificate_path,
            receiver_email,sender_email,password,verbose=False):
    subject = f"Course completion certificate: {course_name}"
    body = f"""\
Dear {student_name},
Congratulations! You have cleared the {course_name} with {student_score} marks out of {total_marks}!
We are excited to share the attached Award of Excellence for your performance!
Regards
{sign_name}"""

    print(f"Sending mail to {student_name}({receiver_email})...")
    mailer_utils.send_mail_with_attachment(subject,body,receiver_email,sender_email,password,
            attachment_file=certificate_path,verbose=verbose)
    print("Done")        

@helpers.internet_check_decorator()
@helpers.log_decorator('certificate_mailer.log')
def create_n_mail_certificates(csv_file_name,course_name,sign_name,total_marks,sender_email,
                mail_interval=2,certi_template = None,
                certi_path='./certificates',overwrite=False,create_certi_only=False,verbose=False):
    
    if certi_template == None: 
        certi_template= os.path.join(os.path.dirname(__file__), 'data/certi_template.jpg')
    try:
        csv_obj = CsvDataIterator(csv_file_name)
        csv_iter = iter(csv_obj)
        header = csv_iter.csv_header
        print('Data header: ',header)
        if header is not None:
            Student = namedtuple('Student',map(lambda x:x.strip(),header))
            if not create_certi_only:
                sender_password = helpers.PasswordHelper(sender_email)
            else:
                sender_password = helpers.PasswordHelper()    

            list(map(partial(_map_func_create_n_mail_certi,tuple_type=Student,course_name = course_name,
                    sign_name=sign_name,total_marks=total_marks,certi_template=certi_template,
                    sender_email= sender_email,sender_password=sender_password,
                    mail_interval=mail_interval,certi_path=certi_path,overwrite=overwrite,
                    create_certi_only=create_certi_only,verbose=verbose),csv_iter))

            return True    
    except StopIteration as e:
        print("Failed!!! Possibly Empty or invalid data file")
    except FileNotFoundError as e:
        print("Failed!!! File not found")         
        return False      
    except TypeError as e:
        print("Failed!!! Invalid Data. Possibly number of fields in data and header don't match")     
    except Exception as e:
        print("Failed!!! ",e)
        return False


