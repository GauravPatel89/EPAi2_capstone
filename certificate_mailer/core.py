# -*- coding: utf-8 -*-
from . import helpers
from . import mailer_utils
import csv
import os
import re
import json
import cv2
import img2pdf
import getpass
from datetime import datetime
import time
from collections import namedtuple
from functools import partial,wraps


__all__ = ['CsvDataIterator', 'create_certificate','create_n_mail_certificates']

# Define an iterator class to read from csv data file
class CsvDataIterator:
    """
    A class to create iterator to read from csv file.
    ...

    Attributes
    ----------
    csv_file_name : str
        csv file to be read

    Methods
    -------
    __iter__():
        Returns iterator to read csv data
    """
    def __init__(self, f_name):
        """
        Constructor for CsvDataIterator class

        Parameters:
            f_name (str): csv file name to be read

        Returns:
            Object of CsvDataIterator class
        """
        self.csv_file_name = f_name

    def __iter__(self):
        """
        Returns an object of class CsvIterator. Using this object
        csv data can be iterated over.

        Parameters:
            None

        Returns:
            Object of CsvIterator class
        """
        return self.CsvIterator(self.csv_file_name)


    class CsvIterator:
        """
        A class to create iterator to read from csv file.
        ...

        Attributes
        ----------
        csv_file_name : str
            csv file to be read

        num_data : int
            Used to keep track of csv data being iterated

        csv_header: list of str
            list of header fields in csv file

        csv_data: list of list of str
            list of lines read from csv file

        data_length: int
            length of csv data excluding header line

        Methods
        -------
        __init__():
            Class constructor

        __iter__():
            Returns reference to itself because class is an iterator

        __next__():
            Returns next line of data from csv file

        is_header_valid():
            Checks csv file header for validity.
        """
        def __init__(self, f_name):
            """
            Constructor for CsvIterator class

            Parameters:
                f_name (str): csv file name to be read

            Returns:
                Object of CsvIterator class
            """
            self.csv_file_name = f_name
            self.num_data = 0
            self.csv_header = None
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
                #print('Data Length:',self.data_length)
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
            """
            Returns reference to itself because class is an iterator

            Parameters:
                None

            Returns:
                self (Ref): Return reference to self
            """            
            return self

        def __next__(self):
            """
            Returns next line of data from csv file or 
            raises StopIteration exception if end
            of file has been reached.

            Parameters:
                None

            Returns:
                data (list of str): Next line of data from csv file
            """
            if self.num_data >= self.data_length:
                raise StopIteration
            else:
                data = self.csv_data[self.num_data]
                self.num_data += 1
                return data

        def is_header_valid(self):
            """
            Checks if header read from csv file is valid.

            Parameters:
                None

            Returns:
                (bool) : Whether csv header is valid
            """                   
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
def create_certificate(student_name:'(str) Name of the student',
                        course_name:'(str) Name of the course',
                        sign_name:'(str) Sign Name',
                        certi_template:'(str) Certificate template file' = None,
                        out_format:'(str) Certificate output file type'='jpg',
                        certi_dir:'(str) Certificate save dirctory'='certificates',
                        overwrite:'(bool) Whether to overwrite certificate if already exists'=False,
                        verbose:'(bool) Verbose'=False):
    """
    Creates a certificate for given student name, course name and sign name of type out_format using
    certi_template as template file and stores it into certi_dir directory

    Parameters:
        student_name(str): Name of the student
        course_name(str): Name of the course
        sign_name(str): Sign Name
        certi_template(str): Certificate template file
        out_format(str): Certificate output file type
        certi_dir(str): Certificate save dirctory
        overwrite(bool): Whether to overwrite certificate if already exists

    Returns:
        certificate_path(str): Path of created certificate
    """

    try:

        if verbose:
            print("***************create_certificate*******************")
        # If certi_template is not passed use a default one
        if certi_template == None: 
            certi_template= os.path.join(os.path.dirname(__file__), 'data/certi_template.jpg')

        if verbose:
            print(f"Certificate template file: {certi_template}")

        # If certi_dir directory does not exist create a new one
        if not os.path.exists(certi_dir):
            print(f'{certi_dir} doesn\'t exist... Creating it...')
            os.mkdir(certi_dir)

        # Generate certificate file name. Whitespaces must be replaced with '_'
        certificate_name = '_'.join(f'{course_name}_{student_name}_{sign_name}.{out_format}'.split())
        # Generate certificate path
        certificate_path = os.path.join(certi_dir,certificate_name)
        if verbose:
            print("Certificate Path",certificate_path)
        # test if certificate for given student,course name, sign exists 

        # if exists and overwrite is False simply return with certificate path
        if (not overwrite) and (os.path.exists(certificate_path)):
            print(f'Certificate {certificate_name} already exists!!! Not creating new....')
            return certificate_path


        if verbose:
            print("Reading ",certi_template)
        # Read certificate image from template image 
        certi_img = cv2.imread(certi_template)

        # load field coordinates
        # Field coordinates are contained json file with name same as template image file
        template_fields_file = '.'.join(certi_template.split('.')[:-1] + ['json'])

        if verbose:
            print("Reading",template_fields_file)
        with open(template_fields_file,"r") as f:
            field_coords = json.load(f)

        if verbose:
            print("Field coordinates")
            print(field_coords)            

        # Select font
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        # Select black color for fonts
        color = (0, 0, 0)

        # Write Course name
        # Get course name coordinates
        course_name_x_start = field_coords["course_name_start"][0]
        course_name_x_end = field_coords["course_name_end"][0]
        course_name_y = field_coords["course_name_start"][1]
        # Set scale and thickness
        course_name_scale = 1
        course_name_thickness = 1

        # Calculate height and width of the text
        (txt_width,_),_ = cv2.getTextSize(course_name,font,course_name_scale,course_name_thickness)
        # Calculate text coordinates such that text center and field center coincide.
        course_name_coords = (int(course_name_x_start +((course_name_x_end-course_name_x_start)/2 - txt_width/2)),course_name_y)


        if verbose:
            print("Writing course name at ",course_name_coords)        
        # Write text into image
        certi_img = cv2.putText(certi_img, course_name, course_name_coords, font,course_name_scale, color, course_name_thickness, cv2.LINE_AA)

        # Write Student name
        # Get Student name coordinates
        student_name_x_start = field_coords["student_name_start"][0]
        student_name_x_end = field_coords["student_name_end"][0]
        student_name_y = field_coords["student_name_start"][1]
        student_name_scale = 1.5
        student_name_thickness = 1

        # Calculate height and width of the text
        (txt_width,_),_ = cv2.getTextSize(student_name,font,student_name_scale,student_name_thickness)
        # Calculate text coordinates such that text center and field center coincide.
        student_name_coords = (int(student_name_x_start +((student_name_x_end-student_name_x_start)/2 - txt_width/2)),student_name_y)

        if verbose:
            print("Writing student name at ",student_name_coords)
        # Write text into image
        certi_img = cv2.putText(certi_img, student_name, student_name_coords, font,student_name_scale, color, student_name_thickness, cv2.LINE_AA)


        # Write Date    
        date_text = datetime.now().strftime("%d %B %Y")

        # Get date coordinates
        date_text_x_start = field_coords["date_start"][0]
        date_text_x_end = field_coords["date_end"][0]
        date_text_y = field_coords["date_start"][1]
        # Set date text scale and thickness
        date_text_scale = 0.75
        date_text_thickness = 1

        # Calculate height and width of the text
        (txt_width,_),_ = cv2.getTextSize(date_text,font,date_text_scale,date_text_thickness)
        # Calculate text coordinates such that text center and field center coincide.
        date_text_coords = (int(date_text_x_start +((date_text_x_end-date_text_x_start)/2 - txt_width/2)),date_text_y)
        if verbose:
            print("Writing date at ",date_text_coords)
        # Write text into image
        certi_img = cv2.putText(certi_img, date_text, date_text_coords, font,date_text_scale, color, date_text_thickness, cv2.LINE_AA)

        # Write Sign name
        # Get sign name coordinates
        sign_name_x_start = field_coords["sign_start"][0]
        sign_name_x_end = field_coords["sign_end"][0]
        sign_name_y = field_coords["date_start"][1]
        # Set sign name scale and thickness
        sign_name_scale = 1
        sign_name_thickness = 1

        # Calculate height and width of the text
        (txt_width,_),_ = cv2.getTextSize(sign_name,font,sign_name_scale,sign_name_thickness)
        # Calculate text coordinates such that text center and field center coincide.
        sign_name_coords = (int(sign_name_x_start +((sign_name_x_end-sign_name_x_start)/2 - txt_width/2)),sign_name_y)
        if verbose:
            print("Writing sign name at ",sign_name_coords)
        # Write text into image
        certi_img = cv2.putText(certi_img, sign_name, sign_name_coords, font,sign_name_scale, color, sign_name_thickness, cv2.LINE_AA)

        if verbose:
            print("Saving image at ",certificate_path)
        # 'pdf' file format needs separate treatment as opencv cannot handle it
        if(out_format == 'pdf'):
            # write image to temporary file
            cv2.imwrite('temp.jpg',certi_img)
            # convert image to pdf
            with open(certificate_path,"wb") as f:
                f.write(img2pdf.convert('temp.jpg'))
            # remove the temporary file
            os.remove('temp.jpg')
        else:
            # save image
            cv2.imwrite(certificate_path,certi_img)
        # return the certificate path
        return certificate_path
    except Exception as e:
        print(f"Failed To create Certificate for {student_name}")
        raise Exception(f"Failed To create Certificate for {student_name}: {e}")

def _map_func_create_n_mail_certi(xx:'(list)Student data',
                                tuple_type:'(type)Type of namedtuple data',
                                course_name:'(str)Course name',
                                sign_name:'(str)Signature name',
                                total_marks:'(float)Total marks in course',
                                sender_email:'(str)Sender\'s email id',
                                sender_password:'(object)Password object for sender email',
                                mail_interval:'(int) Time interval in seconds between consecutive mails',
                                certi_template:'(str) Certificate template file',
                                certi_dir:'(str)Directory path to save created certificates',
                                out_format:'(str)Certificate file format'='jpg',
                                overwrite:'(bool)Whether to overwrite certificates'=False,
                                create_certi_only:'(bool)Only create certificate dont mail'=False,
                                verbose:'(bool)'=False):
    """
    This function, for given student data in xx, creates certificate and mails it.

    Parameters:
        xx(list):Student data
        tuple_type(type):Type of namedtuple data
        course_name(str):Course name
        sign_name(str):Signature name
        total_marks(float):Total marks in course
        sender_email(str):Sender's email id
        sender_password(object): Password object for sender email
        mail_interval(int): Time interval in seconds between consecutive mails
        certi_template(str): Certificate template file
        certi_dir(str): Directory path to save created certificates
        out_format(str): Certificate file format
        overwrite(bool): Whether to overwrite certificates
        create_certi_only(bool): Only create certificate dont mail
        verbose(bool)
    Returns:
        None
    """
    if verbose:
        print("_map_func_create_n_mail_certi:")
    try:
        # Proceed only if data is not empty
        if len(xx) != 0:
            # Convert name into title case
            xx[0] = xx[0].title()
            # Create a namedtuple of tuple_type type
            student = tuple_type(*map(lambda x:x.strip(),xx))
            print('-'*30)
            print(f'Student: Name:{student.name}\t Score:{student.score}\tEmail:{student.email}')

            if verbose:
                print("Performing checks: student name,score,email")
            # student data checks
            # Name : Cannot have Special characters
            if(len(re.findall("[@_!#$%^&*()<>?/\|}{~:]", student.name)) > 0):
                print("Special characters are not allowed in student name")
                return

            # Name : Cannot have numeric characters
            if(len(re.findall("[0-9]", student.name)) > 0):
                print("Numeric characters are not allowed in student name")
                return

            # Score: must be numeric
            if (not student.score.isnumeric()):
                print("Student score must be numeric value")
                return

            # Score: Not more than Total marks
            if (float(student.score) > total_marks):
                print("Student score cannot be more than Total score")
                return

            # Email id: Is valid email id
            if not mailer_utils.is_email_valid(student.email):
                print("Email id is invalid")
                return

            if verbose:
                print('Creating Certificate')
            certificate_path = create_certificate(student_name = student.name, course_name = course_name,
                                sign_name = sign_name,certi_template=certi_template,certi_dir=certi_dir,
                                out_format = out_format,overwrite=overwrite,verbose=verbose)
            print(f'Generated certificate: {certificate_path}')

            # Mail the certificate if selected by user
            if not create_certi_only:
                if verbose:
                    print("Mailing certificate")
                mail_the_certificate(student_name=student.name,student_score=student.score,course_name=course_name,
                        total_marks=total_marks,sign_name=sign_name,certificate_path=certificate_path,
                        receiver_email=student.email,sender_email=sender_email,password=sender_password,verbose=verbose)
                # wait for user selected time period before next iteration
                time.sleep(mail_interval)
    except :
        raise

@helpers.internet_check_decorator()
@helpers.log_decorator('certificate_mailer.log')
def mail_the_certificate(student_name:'(str)Student name',
                        student_score:'(str)Student score',
                        course_name:'(str)Course name',
                        total_marks:'(float)Total marks in the course',
                        sign_name:'(str)Signature name',
                        certificate_path:'(str)Certificate file path to be attached',
                        receiver_email:'(str)Receiver email id',
                        sender_email:'(str)Sender email id',
                        password:'(obj)Password object for sender email id',
                        verbose:'(bool)'=False):
    """
    This function compiles a email message and sends it to student email id along with
    certificate file as an attachment.

    Parameters:
        student_name(str):Student name
        student_score(str):Student score
        course_name(str):Course name
        total_marks(float):Total marks in the course
        sign_name(str):Signature name
        certificate_path(str):Certificate file path to be attached
        receiver_email(str):Receiver email id
        sender_email(str):Sender email id
        password(obj):Password object for sender email id
        verbose(bool):Verbose
    Returns:
        None
    """
    if verbose:
        print("mail_the_certificate:")
        print("Preparing mail subject and body.")
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
def create_n_mail_certificates(csv_file_name:'(str)csv student data file',
                                course_name:'(str)Course name',
                                sign_name:'(str)Signature name',
                                total_marks:'(float)Total marks in the course',
                                sender_email:'(str)Sender email id',
                                mail_interval:'(int)Time interval in seconds between consecutive emails'=2,
                                certi_template:'(str)Certificate template file' = None,
                                certi_dir:'(str)Directory to which created certificates must be saved'='./certificates',
                                out_format:'(str)Certificate file format'='jpg',
                                overwrite:'(bool)Whether to overwrite certificate files'=False,
                                create_certi_only:'(bool)Only create certificates dont mail'=False,
                                verbose:'(bool)Verbose messages'=False):
    """
    This function, for given student data in xx, creates certificate and mails it.

    Parameters:
        csv_file_name(str):csv student data file
        course_name(str):Course name
        sign_name(str):Signature name
        total_marks(str):Total marks in the course
        sender_email(str):Sender email id
        mail_interval(int):Time interval in seconds between consecutive emails
        certi_template(str):Certificate template file
        certi_dir(str):Directory to which created certificates must be saved
        out_format(str):Certificate file format
        overwrite(bool):Whether to overwrite certificate files
        create_certi_only(bool):Only create certificates dont mail
        verbose(bool):Verbose messages
    Returns:
        success(bool): Whether certificates to all the students were successfully sent
    """
    # Perform checks

    if verbose:
        print("******************create_n_mail_certificates********************")
        print("Performing checks: sender email,sign name, total marks,output format")    
    # sender mail must be a valid email id
    if not mailer_utils.is_email_valid(sender_email):
        print("Sender email id is not valid!!!")
        return False

    # sender mail: only gmail allowed
    if "@gmail." not in sender_email:
        print("Sorry!!! We support mail sending through gmail only.")
        return False

    # sign name :cannot have special characters
    if(len(re.findall("[@_!#$%^&*()<>?/\|}{~:]", sign_name)) > 0):
        print("Special characters are not allowed in sign name")
        return False

    # sign name :cannot have numeric characters
    if(len(re.findall("[0-9]", sign_name)) > 0):
        print("Numeric characters are not allowed in sign name")
        return False

    # total marks should not be negative or 0
    if(total_marks <= 0):
        print("Total marks should be nonzero positive number")
        return False

    # Check if output format is valid
    out_format = out_format.lower()
    valid_formats = ['jpg','jpeg','png','bmp','pdf']
    if(out_format not in valid_formats):
        print("Output format is invalid. Select from ",valid_formats)
        return False

    if verbose:
        print("Checking certificate template.")
    # If certificate template has not been passed select default template
    if certi_template == None:
        if verbose:
            print("Certificate template not provided. Using default ")
        certi_template= os.path.join(os.path.dirname(__file__), 'data/certi_template.jpg')

    # Check if json file corresponding to template file exists
    template_fields_file = '.'.join(certi_template.split('.')[:-1] + ['json'])
    if not os.path.exists(template_fields_file):
        print(f"json file corresponding to {certi_template} does not exist.")
        return False

    if verbose:
        print("All checks complete.")
        print("Starting data processing")
    try:
        # Create an object for csv file iteration
        csv_obj = CsvDataIterator(csv_file_name)
        # Obtain an iterator for csv file
        csv_iter = iter(csv_obj)
        # Get the csv file header
        header = csv_iter.csv_header
        if verbose:
            print('Data header: ',header)

        # Don't proceed if header is None 
        if header is not None:
            # Create named tuple object definition using csv header
            Student = namedtuple('Student',map(lambda x:x.strip(),header))
            if verbose:
                print("Named tuple type",Student)
            # Ask user for password using PasswordHelper class. This helps is hiding user password
            # from log files. PasswordHelper class constructor will ask user to enter password
            if not create_certi_only:
                sender_password = helpers.PasswordHelper(sender_email)
            else:
                sender_password = helpers.PasswordHelper()    


            if verbose:
                print("Proceeding with data processing")
            # Since use of for loop or list comprehension is not allowed we make use of 'map'
            # map will iterate over csv_iter and pass that data to _map_func_create_n_mail_certi
            # which will create student certificate and mail it their email id
            list(map(partial(_map_func_create_n_mail_certi,tuple_type=Student,course_name = course_name,
                    sign_name=sign_name,total_marks=total_marks,
                    sender_email= sender_email,sender_password=sender_password,
                    mail_interval=mail_interval,certi_template=certi_template,
                    certi_dir=certi_dir,out_format=out_format, overwrite=overwrite,
                    create_certi_only=create_certi_only,verbose=verbose),csv_iter))

            # If no error so far return True
            return True
        else:
            return False 
    except StopIteration as e:
        print("Failed!!! Possibly Empty or invalid data file")
        return False
    except FileNotFoundError as e:
        print("Failed!!! File not found")         
        return False      
    except TypeError as e:
        print(e)
        print("Failed!!! Invalid Data. Possibly number of fields in data and header don't match")   
        return False  
    except Exception as e:
        print("Failed!!! ")
        print(e)
        return False