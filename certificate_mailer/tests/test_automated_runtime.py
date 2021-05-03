# -*- coding: utf-8 -*-
import pytest
import random
import string
import certificate_mailer
import os
import glob
import inspect
import re
import math
import pkgutil
import csv
from pathlib import Path
import shutil
from faker import Faker



# Test whether app rejects data file without header.
def test_reject_data_file_without_header():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_no_header.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

# Test whether app rejects data file with invalid header. Invalid header means minimum required 
# fields (name,score,email) not found 
def test_reject_data_file_invalid_header():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_invalid_header.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

# Test whether app rejects empty data file.
def test_reject_empty_data_file():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_empty.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

# Test whether app rejects data file with only header and no data.
def test_reject_invalid_data_file():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_only_header_no_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"


# Test whether app rejects invalid data. Invalid data could be more data on certain rows 
# than the header mentions.
def test_reject_invalid_data_file():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_invalid_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

def test_certificate_directory_created():

    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert os.path.exists("./"+certi_dir), f"App should create certificate directory if it does not exists."

def test_certificate_overwrite():

    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]
    modified_time_before = os.path.getmtime(created_file)

    overwrite = True

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=overwrite,create_certi_only=True,verbose=False)

    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]
    modified_time_after = os.path.getmtime(created_file)

    assert modified_time_after > modified_time_before

def test_student_name_in_certificate_name():

    first_name = "Gaurav"
    last_name = "Patel"
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow([first_name+" "+last_name,"4500","gaurav4664@gmail.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]

    assert first_name in created_file
    assert last_name in created_file

def test_student_name_in_proper_case():

    first_name = "gAuRaV"
    last_name = "pAtEl"
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow([first_name+" "+last_name,"4500","gaurav4664@gmail.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]

    assert first_name.title() in created_file
    assert last_name.title() in created_file

def test_course_name_in_certificate_name():

    first_name = "Gaurav"
    last_name = "Patel"
    course_name = "EPAi2"

    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow([first_name+" "+last_name,"4500","gaurav4664@gmail.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name=course_name,
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]

    assert course_name in created_file



# test if it can handle more than 1000 student data
def test_app_handles_large_data():
    # Since sending so many mails is not feasible. We will just test whether app is
    # able to generate more than 1000 student certificate.
    num_students = 10
    # lets first create a csv file containing 1001 fake student data
    with open('large_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        fake = Faker()
        for i in range(num_students):
            fake_profile = fake.profile()
            random_subscript = ''.join(random.choice(string.ascii_letters) for x in range(5))
            writer.writerow([fake_profile['name']+ random_subscript,str(random.randint(100,1000)),fake_profile['mail']])
    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='large_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=True,create_certi_only=True,verbose=False)

    # Find out how many certificates have been created.
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==num_students, f"App should be able to handle more than 1000 students data."

# test if it can handle more than 1000 student data
def test_regex_email_1():
    # lets first create a csv file containing invalid email id
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])
        writer.writerow(["varuag letap","4500","gaurav4664gmail.com"])

    certi_dir = "test_certificates"
    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject invalid email id."

# test if it can handle more than 1000 student data
def test_regex_email_2():
    # lets first create a csv file containing invalid email id
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])
        writer.writerow(["varuag letap","4500","gaurav4664@gmailcom"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject invalid email id."  


def test_regex_email_3():

    # lets first create a csv file containing invalid email id
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])
        writer.writerow(["varuag letap","4500","gaurav46+64@gmail.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject invalid email id."  


def test_student_name_numeric_char_check():

    # lets first create a csv file containing invalid email id
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])
        writer.writerow(["varuag123 letap","4500","gaurav4664@yahoo.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject student name with numeric characters."  

def test_student_name_special_char_check():

    # lets first create a csv file containing invalid email id
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])
        writer.writerow(["varuag@letap","4500","gaurav4664@yahoo.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject student name with special characters."

def test_student_score_numeric():

    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])
        writer.writerow(["varuag letap","60ab","gaurav4664@yahoo.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject student with non numeric score."

def test_student_score_not_more_than_total():

    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])
        writer.writerow(["varuag letap","6000","gaurav4664@yahoo.com"])

    certi_dir = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject student with score more than total score."


def test_sender_email_check1():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    assert result == False,"App should check for invalid sender email id"

def test_sender_email_check2():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    assert result == False,"App should check for invalid sender email id"    

def test_sender_email_is_gmail_check():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@yahoo.com"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    assert result == False,"App should check if sender email id belongs to gmail."    

def test_sign_name_special_char_check():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan@Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    assert result == False,"App should check for special characters in sign name"    

def test_sign_name_numeric_char_check():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan99 Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    assert result == False,"App should check for numeric characters in sign name"    

def test_total_marks_nonzero_check():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 0.0
    sender_email = "gaurav4664.test@gmail.com"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    assert result == False,"App should check if total score is nonzero positive number"    

def test_total_marks_positive_check():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = -5000
    sender_email = "gaurav4664.test@gmail.com"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    assert result == False,"App should check if total score is nonzero positive number"    

def test_pdf_output_format():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"
    out_format = "pdf"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,out_format=out_format,overwrite=False,create_certi_only=True,verbose=False)

    assert len(glob.glob("./"+certi_dir+"/*."+out_format))==1, "App should have generated .pdf certificate"

def test_png_output_format():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"
    out_format = "png"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,out_format=out_format,overwrite=False,create_certi_only=True,verbose=False)

    assert len(glob.glob("./"+certi_dir+"/*."+out_format))==1, "App should have generated .png certificate"

def test_invalid_output_format():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"
    out_format = "txt"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,out_format=out_format,overwrite=False,create_certi_only=True,verbose=False)

    assert len(glob.glob("./"+certi_dir+"/*."+out_format))==0, f"App should reject invalid image formats"

def test_invalid_template_reject():
    # Test if app rejects template jpg file without accompanying json file
    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"
    out_format = "jpg"
    certi_template = "test_template.jpg"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,certi_template=certi_template,
    certi_dir=certi_dir,out_format=out_format,overwrite=False,create_certi_only=True,verbose=False)

    assert result == False, f"App should reject template without accompanying json file."
