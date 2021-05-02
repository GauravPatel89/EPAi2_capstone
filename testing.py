import certificate_mailer
import csv
from faker import Faker
import random
import json
import re
from pathlib import Path
import glob

def test_student_score_not_more_than_total():

    with open('temp_data.csv',"w") as f:
        writer = csv.writer(f)
        writer.writerow(["name","score","email"])
        writer.writerow(["gaurav patel","4500","gaurav4664@gmail.com"])
        writer.writerow(["varuag letap","6000","gaurav4664@gmail.com"])

    certi_path = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_path)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='temp_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_path=certi_path,overwrite=False,create_certi_only=True,verbose=False)

    # Only one certificate should be created
    assert len(glob.glob("./"+certi_path+"/*.jpg"))==1, f"App should reject student with score more than total score."

test_student_score_not_more_than_total()

# def test_indentations(filename):
#     ''' Returns pass if used four spaces for each level of syntactically \
#     significant indenting.'''
#     # list all the files is current directory
#     # files = glob.glob("./" + '/**/*.py', recursive=True)
#     # Now for each of the files check if line starts with 'for' or 'while' and ends with ':'.
#     # for f in files:
#     #     if f.find('test') == -1:
#     with open(filename) as fid:
#         contents = fid.read()
#         spaces = re.findall('\n +.', contents)
#         for i,space in enumerate(spaces):
#             print(i,space,len(space))
#             assert len(space) % 4 == 2, f"Your script contains misplaced indentations{space}"
#             assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"

# test_indentations('./certificate_mailer/tests/test_automated.py')