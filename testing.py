import certificate_mailer
import csv
from faker import Faker
import random
import json

template = {
    "course_name_start" : (332,306),
    "course_name_end" : (712,306),
    "student_name_start" : (345,450),
    "student_name_end" : (685,450),
    "date_start" : (196,532),
    "date_end" : (422,532),
    "sign_start" : (626,532),
    "sign_end" : (854,532),
}


# def generate_data(n):
#     with open('large_data.csv',"w") as f:
#         writer = csv.writer(f)
#         writer.writerow(["name","score","email"])
#         fake = Faker()
#         for i in range(n):
#             fake_profile = fake.profile()
#             writer.writerow([fake_profile['name'],str(random.randint(100,1000)),fake_profile['mail']])


# generate_data(5)
# def internetOnOrNot():
#     def dec(fn):
#         def inner(*args, **kwargs):
#             return fn(*args, **kwargs)
#         return inner
        
#     if (certificate_mailer.is_internet_connected()):
#         return dec
#     else:
#         print("Not connected to Internet!!! Please connect to network...")
#         raise Exception("Disconnected from Network!!!")

# @internetOnOrNot()
# def hello_world(n):
#     for i in range(n):
#         print(i,"Hello World")    
#     return True

# hello_world(5)
# import logging

# def setup_logging(name="logger",filepath=None,stream_log_level="DEBUG",file_log_level="DEBUG"):
    
#     logger = logging.getLogger(name)
#     logger.setLevel("DEBUG")
#     formatter = logging.Formatter(
#         '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )    
    
#     if filepath is not None:
#         fh = logging.FileHandler(filepath)
#         fh.setLevel(getattr(logging, file_log_level))
#         fh.setFormatter(formatter)
#         logger.addHandler(fh)    
#         return logger
        

# def log_decorator(log_name):
#     def log_this(function):
#         logger = setup_logging(log_name,'logger.log')
#         def new_function(*args,**kwargs):
#             logger.debug(f"{function.__name__} - {args} - {kwargs}")
#             try:
#                 output = function(*args,**kwargs)
#                 logger.debug(f"{function.__name__} returned: {output}")
#                 return output
#             except Exception as e:
#                 logger.exception(f"{function.__name__}: Exception:{e}")
#                 raise e
#         return new_function
#     return log_this        

# @log_decorator('test_logging')
# def hello_world(n):
#     for i in range(n):
#         print(i,"Hello World")    
#     raise RuntimeError
#     return True

# hello_world(5)    