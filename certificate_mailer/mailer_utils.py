import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ntpath
import os
import re

from . import helpers



__all__ = ['send_mail_with_attachment','send_mail','is_email_valid']

 
def is_email_valid(email:'(str)Email id to be checked'):
    """
    Function to check if given email id is valid.

    Parameters:
        email (str): Email id to be checked

    Returns:
        validity(bool): Email id is valid or not
    """
    # Create regex pattern for valid email id.
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    # if structure defined in regex is found email id is valid
    if(re.search(regex, email)):
        return True
    else:
        return False


@helpers.internet_check_decorator()
@helpers.log_decorator('certificate_mailer.log')
def send_mail_with_attachment(subject:'(str)Email subject text',
                            body:'(str)Email body text',
                            receiver_email:'(str)Receiver email id',
                            sender_email:'(str)Sender email id',
                            password:'(obj)PasswordHelper object',
                            attachment_file:'(str)Attachment file'=None,
                            verbose:'(str)Verbose'=False):
    """
    Function compiles an email with given subject, body and attachment file and
    sends it to receiver email id using sender's credentials.

    Parameters:
        subject(str):Email subject text
        body(str):Email body text
        receiver_email(str):Receiver email id
        sender_email(str):Sender email id
        password(obj):PasswordHelper object
        attachment_file(str):Attachment file
        verbose(str):Verbose
    Returns:
        None
    """
    if verbose:
        print("send_mail_with_attachment:")
    try:
        if (not attachment_file) or (not os.path.exists(attachment_file)):
            print(f'Attachment file: {attachment_file} does not exist. Can\'t send the mail.')
            raise FileNotFoundError

        if verbose:
            print("Creating email message")
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        if verbose:
            print("Attaching ",attachment_file)
        # Open PDF file in binary mode
        with open(attachment_file, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {ntpath.basename(attachment_file)}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        if verbose:
            print(f"Sending mail to {receiver_email}...")
        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password.password)
            server.sendmail(sender_email, receiver_email, text)

        if verbose:
            print("Done")     
    except :
        print("Failed while sending the mail")
        raise

@helpers.internet_check_decorator()
@helpers.log_decorator('certificate_mailer.log')
def send_mail(subject:'(str) Email subject text',
                body:'(str) Email body text',
                receiver_email:'(str) Receiver email id',
                sender_email:'(str) Sender email id',
                password:'(obj) PasswordHelper object',
                verbose:'(bool)'=False):
    """
    Function compiles an email with given subject, body and attachment file and
    sends it to receiver email id using sender's credentials.

    Parameters:
        subject(str):Email subject text
        body(str):Email body text
        receiver_email(str):Receiver email id
        sender_email(str):Sender email id
        password(obj):PasswordHelper object
        verbose(str):Verbose
    Returns:
        None
    """
    try:
        message = f"""\
    Subject: {subject}

    {body}"""
        print(f"Sending mail to {receiver_email}...")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password.password)
            server.sendmail(sender_email, receiver_email, message)
    except:
        print("Failed while sending the mail")
        raise