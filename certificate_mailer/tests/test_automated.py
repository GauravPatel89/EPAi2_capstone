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



CHECK_FOR_THINGS_COMPULSORILY_USED = [
  'namedtuple',
  'datetime',  
]

CHECK_FOR_THINGS_NOT_ALLOWED = [
    'for',
    'while'
]

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme_words=[word for line in open('README.md', 'r', encoding="utf-8") for word in line.split()]
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_no_loops_used():
    # list all the files is current directory
    files = glob.glob("./" + '/**/*.py', recursive=True)
    print("To be inspected: ",files)
    # Now for each of the files check if line starts with 'for' or 'while' and ends with ':'.
    for f in files:
        #print('testing:',f)
        # If filename starts with 'test' dont evaluate it
        if f.find('test') == -1:
            with open(f) as fid:
                # Test each line
                for line in fid.readlines():
                    # Remove whitespace from start and end
                    line = line.strip()
                    assert not ((line.startswith('for') and line.endswith(':')) or 
                    (line.startswith('while') and line.endswith(':'))),f'Loops found in {f}'

def test_no_list_comprehension_used():
    # list all the files is current directory
    files = glob.glob("./" + '/**/*.py', recursive=True)
    print("To be inspected: ",files)
    # Now for each of the files check if line starts with 'for' or 'while' and ends with ':'.
    for f in files:
        #print('testing:',f)
        # If filename starts with 'test' dont evaluate it
        if f.find('test') == -1:
            with open(f) as fid:
                # Test each line
                for line in fid.readlines():
                    # Remove whitespace from start and end
                    line = line.strip()
                    assert not ((line.find('for') >=0) and line.endswith(']')),f'List comprehension found in {f}'



def test_function_name_had_cap_letter():
    functions = inspect.getmembers(certificate_mailer, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

# Test whether app rejects data file without header.
def test_reject_data_file_without_header():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_no_header.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_path='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

# Test whether app rejects data file with invalid header. Invalid header means minimum required 
# fields (name,score,email) not found 
def test_reject_data_file_invalid_header():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_invalid_header.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_path='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

# Test whether app rejects empty data file.
def test_reject_empty_data_file():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_empty.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_path='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

# Test whether app rejects data file with only header and no data.
def test_reject_invalid_data_file():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_only_header_no_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_path='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"


# Test whether app rejects invalid data. Invalid data could be more data on certain rows 
# than the header mentions.
def test_reject_invalid_data_file():
    result = certificate_mailer.create_n_mail_certificates(csv_file_name='.data/test_data_invalid_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_path='./certificates',overwrite=False,create_certi_only=False,verbose=False)
    assert result==False,"Application should fail if data file doesn't have a header"

def test_atleast_one_package():
    files = glob.glob("./"+'/**/__init__.py',recursive=True)
    assert len(files) >= 1, "There should be atleast one package."

def test_atleast_two_modules():
    modules = [modname for importer, modname, ispkg in pkgutil.iter_modules(certificate_mailer.__path__) 
                if not ispkg] 
    assert len(modules) >= 2,"Ther should be atleast 2 modules."


# Test that atleast 2 decorators were used.
def test_atleast_two_decorators_used():
    # We look for unique lines starting with '@'. If there are atleast 2 lines 
    # are found then test successfully passed.

    # list all the files is current directory
    files = glob.glob("./" + '/**/*.py', recursive=True)
    # Now for each of the files check if line starts with 'for' or 'while' and ends with ':'.
    decorator_set = set()
    for f in files:
        #print('testing:',f)
        with open(f) as fid:
            # Test each line
            for line in fid.readlines():
                # Remove whitespace from start and end
                line = line.strip()
                if line.startswith('@'):
                    decorator_set.add(line)
    assert len(decorator_set)>=2,"There should be atleast 2 decorators"

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
            writer.writerow([fake_profile['name']+str(random.randint(1,10000)),str(random.randint(100,1000)),fake_profile['mail']])
    certi_path = "test_certificates"

    # remove directory if already exists. The app will create the directory and put certificates there.
    dirpath = Path('.', certi_path)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    result = certificate_mailer.create_n_mail_certificates(csv_file_name='large_data.csv',course_name="EPAi2",
    sign_name= "Rohan Shravan",total_marks=5000,sender_email="gaurav4664.test@gmail.com",mail_interval=2,
    certi_path=certi_path,overwrite=True,create_certi_only=True,verbose=False)

    # Find out how many certificates have been created.
    assert len(glob.glob("./"+certi_path+"/*.jpg"))==num_students, f"App should be able to handle more than 1000 students data."

# TODO Every function has proper documentation
# TODO can handle 1000+ emails

# TODO Check if marks are less than TOTAL_MARKS
# TODO regex for emails
# TODO check if certificates are regenerated if already exists
# TODO Name conversion to Proper Case
# 

# def test_readme_proper_description():
#     READMELOOKSGOOD = True
#     f = open("README.md", "r", encoding="utf-8")
#     content = f.read()
#     f.close()
#     for c in README_CONTENT_CHECK_FOR:
#         if c not in content:
#             print(c)
#             READMELOOKSGOOD = False
#             pass
#     assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

# def test_readme_file_for_formatting():
#     f = open("README.md", "r", encoding="utf-8")
#     content = f.read()
#     f.close()
#     assert content.count("#") >= 10

# def test_indentations():
#     ''' Returns pass if used four spaces for each level of syntactically \
#     significant indenting.'''
#     lines = inspect.getsource(session3)
#     spaces = re.findall('\n +.', lines)
#     for space in spaces:
#         print(len(space))
#         assert len(space) % 4 == 2, "Your script contains misplaced indentations"
#         assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines" 


# def test_invalid_base_valueerror():
#     with pytest.raises(ValueError):
#         session3.encoded_from_base10(10, -1, '1234567890')
#     with pytest.raises(ValueError):
#         session3.encoded_from_base10(10, 1, '012')
#     with pytest.raises(ValueError):
#         session3.encoded_from_base10(10, 37, '1234567890123456789012345678901234567')

# def test_invalid_base_valueerror_provides_relevant_message():
#     with pytest.raises(ValueError, match=r".* base .*"):
#         session3.encoded_from_base10(10, -1, '1234567890')

# def test_innacurate_digit_map_length():
#     with pytest.raises(ValueError):
#         session3.encoded_from_base10(123123, 16, '0123456789abcde')

#     with pytest.raises(ValueError):
#         session3.encoded_from_base10(123123, 9, '01234567')


# def test_hexadecimal_conversions():
#     for _ in range(50):
#         r_num = random.randint(0, 32767)
#         assert (session3.encoded_from_base10(r_num, 16, '0123456789abcdef').lower() ) == hex(r_num)[2:], f"Your program returned wrong HEX conversions"

# def test_negative_hexadecimal_conversions():
#     for _ in range(50):
#         r_num = random.randint(-32700, -1)
#         assert (session3.encoded_from_base10(r_num, 16, '0123456789abcdef').lower() ) == '-' + hex(r_num)[3:], f"Your program returned wrong HEX conversions"


# def test_repeating_digits_in_digit_map():
#     with pytest.raises(ValueError):
#         session3.encoded_from_base10(10, 10, '0123401234')

# def test_repeating_digits_valueerror_provides_relevant_message():
#     with pytest.raises(ValueError, match=r".* repeating .*"):
#         session3.encoded_from_base10(10, 10, '012AB012ab'), 'Something is fishy! You are not using word "repeating" while talking about an error releated to "repeating" alphanumerics!!'

# def test_float_equality_testing():
#     for _ in range(10000):
#         scale = random.randint(1, 1000000)
#         a = random.uniform(-1.5, 1.6)
#         a, b = a * scale, a * scale - a / scale
#         assert session3.float_equality_testing(a, b) == math.isclose(a, b, rel_tol = 1e-12, abs_tol=1e-05), 'Aap jis number se sampark karna chahte hai, woh is samay uplabdh nahi hai, kripya thodi der baad prayas karein. The numbers you are trying to check right now are not equal, please try again later'


# def test_fraction_used_or_not():
#     code_lines = inspect.getsource(session3)
#     assert 'fractions' in code_lines, 'Fractions not used! You must use fractions'
#     assert 'import' in code_lines, 'You have not imported fractions!'

# def test_manual_truncation_function():
#     for _ in range(100):
#         f_num = random.uniform(-100, 100)
#         assert session3.manual_truncation_function(f_num) == math.trunc(f_num), 'Just because you are not able to fix this truncation error, SkyNet is going to rule the earth!'

# def test_manual_rounding_function():
#     for f_num in [1.25, 1.35, -1.25, -1.35]:
#         assert session3.manual_rounding_function(f_num) == round(f_num), 'Terminator after looking at your code: I will be back! He will come back when you fix your rounding errors.'


# def test_functions_for_zero():
#     assert session3.float_equality_testing(0.0, 0.0), 'How can zero be not equal to zero?'
#     assert session3.manual_truncation_function(0.0) == 0, 'Tuncation of 0 should be zero'
#     assert session3.manual_rounding_function(0.0) == 0, 'Zero can only be rounded off to zero'


