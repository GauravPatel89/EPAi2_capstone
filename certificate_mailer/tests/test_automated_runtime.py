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

    # Generate a temporary csv file without header
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=True,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

# Test whether app rejects data file with invalid header. Invalid header means minimum required 
# fields (name,score,email) not found 
def test_reject_data_file_invalid_header():

    # Generate a temporary csv file with invalid header
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=True,verbose=False)
    assert result==False,"Application should fail if data file has invalid header"

# Test whether app rejects empty data file.
def test_reject_empty_data_file():

    # Generate a temporary empty csv file
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=True,verbose=False)
    assert result==False,"Application should fail if data file is empty"

# Test whether app rejects data file with only header and no data.
def test_reject_header_only_data_file():

    # Generate a temporary csv file with header only
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=True,verbose=False)
    assert result==False,"Application should fail if data file has only header no data"


# Test whether app rejects invalid data. Invalid data could be more data on certain rows 
# than the header mentions.
def test_reject_invalid_data_file():

    # Generate a temporary csv file with invalid data. Row with more data then fields in header
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com","12345678"])

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir='./certificates',overwrite=False,create_certi_only=True,verbose=False)
    assert result==False,"Application should fail if data file contains invalid data"

# Test if certificate directory is created by the application if doesn't exist.
def test_certificate_directory_created():

    # Generate a temporary csv file
    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])


    certi_dir = "test_certificates"

    # remove directory if already exists. The app should create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # Check if directory has been created
    assert os.path.exists("./"+certi_dir), f"App should create certificate directory if it does not exists."

# Test if selecting "overwrite" flag overwrites already created certificates
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

    # Call the app
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]

    # Note last modified time for generated certificate.
    modified_time_before = os.path.getmtime(created_file)

    # Select overwrite option
    overwrite = True

    # Call the app again
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_dir=certi_dir,overwrite=overwrite,create_certi_only=True,verbose=False)

    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]
    # Note the last modified time for generated certificate.
    modified_time_after = os.path.getmtime(created_file)

    # last modified time of certificate file after second call should
    # be later than first call hence suggesting overwrite.
    assert modified_time_after > modified_time_before,"Overwrite option should overwrite preexisting certificate files"

# Test if student name is part of generated certificate filename
def test_student_name_in_certificate_name():

    first_name = "Gaurav"
    last_name = "Patel"

    # Create a temporary data file containing above student name
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

    # Find the filename of generated certificate.
    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]

    # check if student name is contained in the certificate file name
    assert first_name in created_file,"Student name should be part of certificate file name"
    assert last_name in created_file,"Student name should be part of certificate file name"


# Check if student name is in proper case 
def test_student_name_in_proper_case():

    # Student name if random case.
    first_name = "gAuRaV"
    last_name = "pAtEl"
    # Create a temporary data file containing above student name
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

    # Find the name of generated certificate file. 
    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]

    # Name printed in the certificate is used in file name also. Check it.
    assert first_name.title() in created_file,"Student name should be in proper case"
    assert last_name.title() in created_file,"Student name should be in proper case"

# check if course name is part of certificate file name
def test_course_name_in_certificate_name():

    # Set the student and course name
    first_name = "Gaurav"
    last_name = "Patel"
    course_name = "EPAi2"

    # Create a temporary csv data file
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

    # find the name of generated certificate file.
    created_file = glob.glob("./"+certi_dir+"/*.jpg")[0]
    # check if course name is part of certificate file name
    assert course_name in created_file,"Course name should be part of certificate file name"



# test if it can handle more than 1000 student data
def test_app_handles_large_data():
    # Since sending so many mails is not feasible. We will just test whether app is
    # able to generate more than 1000 student certificate.
    num_students = 1001
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

# test if app rejects invalid student email id
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

    # Since only one student data is valid, only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject invalid email id."

# test if app rejects invalid student email id
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

    # Since only one student data is valid, only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject invalid email id."  

# test if app rejects invalid student email id
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

    # Since only one student data is valid, only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject invalid email id."  

# App should reject numeric characters in student name
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

    # Since only one student data is valid, only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject student name with numeric characters."  

# App should reject special characters in student name
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

    # Since only one student data is valid, only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject student name with special characters."

# App should reject non-numeric student score
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

    # Since only one student data is valid, only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject student with non numeric score."

# App should reject student with score more than total course marks
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

    # Since only one student data is valid, only one certificate should be created
    assert len(glob.glob("./"+certi_dir+"/*.jpg"))==1, f"App should reject student with score more than total score."

# App should check if sender email is valid
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

    # app should fail since sender mail is not valid
    assert result == False,"App should check for invalid sender email id"

# App should check if sender email is valid
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
    # app should fail since sender mail id is not valid
    assert result == False,"App should check for invalid sender email id"    

# App must not accept non gmail email id as sender email id
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

    # app should fail because sender email is not a gmail id.
    assert result == False,"App should check if sender email id belongs to gmail."    

# Check if app rejects special characters in sign name
def test_sign_name_special_char_check():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan@Shravan" # Sign name with special name
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)
    # App should fail for sign name with special characters
    assert result == False,"App should check for special characters in sign name"    

# checkk if app fails for sign name with numeric characters.
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
    # App should fail for sign name with numeric characters.
    assert result == False,"App should check for numeric characters in sign name"    

# Check if app rejects total marks being zero
def test_total_marks_nonzero_check():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 0.0   # total marks as 0
    sender_email = "gaurav4664.test@gmail.com"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)

    # App should fail for zero total marks.
    assert result == False,"App should check if total score is nonzero positive number"    

# Check if app rejects negative total marks.
def test_total_marks_positive_check():

    csv_file_name = "test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = -5000         # Negative total marks.
    sender_email = "gaurav4664.test@gmail.com"

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,overwrite=False,create_certi_only=True,verbose=False)
    # App should fail for negative totall marks.
    assert result == False,"App should check if total score is nonzero positive number"    

# Test if app is able to generate pdf file format
def test_pdf_output_format():

    csv_file_name = "certificate_mailer/data/test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"
    out_format = "pdf"  # Output file format is pdf

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,out_format=out_format,overwrite=False,create_certi_only=True,verbose=False)

    # The app should generate pdf certificate files.
    assert len(glob.glob("./"+certi_dir+"/*."+out_format))>0, "App should have generated .pdf certificate"

# Test if app is able to generate png file format
def test_png_output_format():

    csv_file_name = "certificate_mailer/data/test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"
    out_format = "png"  # output file format is png

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,out_format=out_format,overwrite=False,create_certi_only=True,verbose=False)

    # app should generate png certificte files
    assert len(glob.glob("./"+certi_dir+"/*."+out_format))>0, "App should have generated .png certificate"

# Check if app rejects invalid output file formats.
def test_invalid_output_format():

    csv_file_name = "certificate_mailer/data/test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"
    out_format = "txt"      # invalid output file format 'txt'

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,
    certi_dir=certi_dir,out_format=out_format,overwrite=False,create_certi_only=True,verbose=False)

    # App should fail for invalid output file format
    assert result==False, f"App should reject invalid image output formats"

# Test if app rejects template jpg file without accompanying json file 
def test_invalid_template_reject():

    csv_file_name = "certificate_mailer/data/test_data.csv"
    certi_dir = "test_certificates"
    sign_name = "Rohan Shravan"
    course_name = "EPAi2"
    total_marks = 5000
    sender_email = "gaurav4664.test@gmail.com"
    out_format = "jpg"
    certi_template = "test_template.jpg"    #certificate template file without coordinate json file

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_dir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name=csv_file_name,course_name=course_name,
    sign_name= sign_name,total_marks=total_marks,sender_email=sender_email,mail_interval=2,certi_template=certi_template,
    certi_dir=certi_dir,out_format=out_format,overwrite=False,create_certi_only=True,verbose=False)

    # App shpuld fail since the certificate template file does not exist
    assert result == False, f"App should reject template without accompanying json file."
