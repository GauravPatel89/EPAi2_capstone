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



README_CONTENT_CHECK_FOR = [
    'Usage',
    'template',  
]

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme_words=[word for line in open('README.md', 'r', encoding="utf-8") for word in line.split()]
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10  

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            print(c)
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"


def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    # list all the files is current directory
    files = glob.glob("./" + '/**/*.py', recursive=True)
    # Now for each of the files check if line starts with 'for' or 'while' and ends with ':'.
    for f in files:
        #print("Testing ",f)
        with open(f) as fid:
            contents = fid.read()
            spaces = re.findall('\n +.', contents)
            for space in spaces:
                #print(space,len(space))
                assert len(space) % 4 == 2, f"Your script contains misplaced indentations"
                assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"    


def test_namedtuple_used():
    # list all the files is current directory
    files = glob.glob("./" + '/**/*.py', recursive=True)
    # Now for each of the files check if line starts with 'for' or 'while' and ends with ':'.
    namedtuple_used = False
    for f in files:
        # If filename starts with 'test' dont evaluate it
        if f.find('test') == -1:
            with open(f) as fid:
                contents = fid.read()
                namedtuple_used = namedtuple_used or ('namedtuple' in contents)

    assert namedtuple_used, "namedtuple is not used in the app"


def test_datetime_used():
    # list all the files is current directory
    files = glob.glob("./" + '/**/*.py', recursive=True)
    # Now for each of the files check if line starts with 'for' or 'while' and ends with ':'.
    datetime_used = False
    for f in files:
        # If filename starts with 'test' dont evaluate it
        if f.find('test') == -1:
            with open(f) as fid:
                contents = fid.read()
                datetime_used = datetime_used or ('datetime' in contents)

    assert datetime_used, "datetime is not used in the app"

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

def test_requirements_file_exists():
    assert os.path.isfile("requirements.txt"), "requirements.txt file missing!"

def test_license_file_exists():
    assert os.path.isfile("LICENSE"), "LICENSE is missing!"

# TODO Every function has proper documentation
def test_every_function_has_documentation():
    list_functions = inspect.getmembers(certificate_mailer,inspect.isfunction)
    for fn in list_functions:
        print(fn)
        assert fn[1].__doc__ != None , f"{fn[0]}: Doc string Missing"
        assert len(fn[1].__doc__) > 25, f"{fn[0]}: Doc string too small. Describe function properly"

def test_every_function_has_annotation():
    list_functions = inspect.getmembers(certificate_mailer,inspect.isfunction)
    for fn in list_functions:
        print(fn)
        assert len(fn[1].__annotations__) > 0, f"{fn[0]}: Annotation missing"        