import logging
import os
import socket
from datetime import datetime
import getpass
from functools import wraps

__all__ = ['log_decorator','internet_check_decorator','PasswordHelper']

class PasswordHelper:
    """
    A class to manage user password.
    ...

    Attributes
    ----------
    sender_email : str
        Sender's email id
    password: str
        Sender's password

    Methods
    -------
    __init__():
        Class constructor 
    """
    def __init__(self,sender_email=None):
        """
        Class constructor. Asks user for email password and saves it.

        Parameters:
            sender_mail(str): Sender email id

        Returns:
            class object

        """
        self.sender_email = sender_email
        self.password = None
        if self.sender_email:
            self.password = getpass.getpass(f"Please Enter Password for {self.sender_email}...")


def log_to_file(file_name:'(str)file name',msg:'(str)Message to be appended to the file'):
    """
    This function appends given message to given log file.
    Parameters:
        file_name(str): Log file name
        msg(str): Message to be appended to log file
    Returns:
        None
    """
    # Get current time and date in the form of string
    date_time_str = datetime.now().strftime("[%d/%m/%Y, %H:%M:%S.%f] ")
    # Open file in append mode and write message into it with proper datetime stamp
    with open(file_name,mode="a+") as fid:
        fid.write("\n" + date_time_str + msg+"\n")


def log_decorator(log_file_name:'(str)Log file name'='default.log'):
    """
    This function acts as a decorator factory. Returns a decorator
    to log function call and return.
    Parameters:
        log_file_name(str): Log file name
    Returns:
        decorator: decorator to log function calls and returns
    """
    def log_this(function):
        @wraps(function)
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
    """
    Function to check if internet is connected.
    Parameters:
        None
    Returns:
        bool: Is internet connected
    """
    try:
        # connect to the host -- tells us if the host is actually  reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

def internet_check_decorator() -> 'decorator':
    """
    Decorator factory to check if internet is connected before calling
    a function. If iternet is not connected decorator will provide dummy function
    which returns False no matter what the arguments.
    """
    def dec(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)
        return inner

    def dec_failure(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            return False
        return inner

    if (is_internet_connected()):
        return dec
    else:
        print("Not connected to Internet!!! Please connect to network...")
        return dec_failure