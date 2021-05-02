import logging
import os
import socket
from datetime import datetime
import getpass

__all__ = ['log_decorator','internet_check_decorator','PasswordHelper']

class PasswordHelper:
    def __init__(self,sender_email=None):
        self.sender_email = sender_email
        self.password = None
        if self.sender_email:
            self.password = getpass.getpass(f"Please Enter Password for {self.sender_email}...")


def log_to_file(file_name,msg):
    date_time_str = datetime.now().strftime("[%d/%m/%Y, %H:%M:%S.%f] ")
    with open(file_name,mode="a+") as fid:
        fid.write("\n" + date_time_str + msg+"\n")


def log_decorator(log_file_name='default.log'):
    def log_this(function):
        def new_function(*args,**kwargs):
            log_to_file(log_file_name,f"{function.__name__} - {args} - {kwargs}")
            try:
                output = function(*args,**kwargs)
                log_to_file(log_file_name,f"{function.__name__} returned: {output}")
                return output
            except Exception as e:
                log_to_file(log_file_name,f"ERROR: {function.__name__}: Exception:{e}")
                raise e
        return new_function
    return log_this


def is_internet_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

def internet_check_decorator():
    def dec(fn):
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)
        return inner

    def dec_failure(fn):
        def inner(*args, **kwargs):
            return False
        return inner

    if (is_internet_connected()):
        return dec
    else:
        print("Not connected to Internet!!! Please connect to network...")
        return dec_failure