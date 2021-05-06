# EPAi2 Capstone Project

## certificate_mailer  

This project implements a certificate generation and mailing app. User has to provide a csv file containing student data (name,score,email id etc). The app will generate a certificate for all the students using user selecteable certificate template and mail it to their respective email ids.

### Submission:
The final submission output can be found in [Results](https://github.com/GauravPatel89/EPAi2_capstone/tree/main/Results) directory. [Application](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/certificate_mailer_app.py) was run on [data.csv](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/Results/data.csv) file. Generated certificates were stored in [certificates](https://github.com/GauravPatel89/EPAi2_capstone/tree/main/Results/certificates) directory. The certificates were also mailed to student email ids. Screenshots showing the gmail inbox can be found here([1](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/Results/Submission_Screenshot1.png),[2](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/Results/Submission_Screenshot2.png),[3](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/Results/Submission_Screenshot3.png)). This submission run is shown below. 

![submission1.gif](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/Results/submission1.gif)

#### Installation:  

1.Clone the repository  
      
      git clone https://github.com/GauravPatel89/EPAi2_capstone.git
      cd EPAi2_capstone
      
2.Install the dependencies

      pip install -r requirements.txt
      
#### Usage:  
We have provided an example usage in [certificate_mailer_app.py](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/certificate_mailer_app.py).
It can be used as follow.

- Check app help

      python certificate_mailer_app.py -h
      
      usage: certificate_mailer_app.py [-h] [-t CERTI_TEMPLATE] [-d CERTI_DIR] [-f OUT_FORMAT] [-o] [-c] [-i INTERVAL] [-v]
                                 csv_file course_name sign_name total_marks sender_email

      positional arguments:
        csv_file              csv file containing the student data
        course_name           Name of the course
        sign_name             Signature name to be printed on certificate
        total_marks           Total marks in the course
        sender_email          Email id of sender. Password will be asked later

      optional arguments:
        -h, --help            show this help message and exit
        -t CERTI_TEMPLATE, --certi_template CERTI_TEMPLATE
                              Path where created certificates will be saved. (Default:
                              './certificate_mailer/data/certi_template.jpg')
        -d CERTI_DIR, --certi_dir CERTI_DIR
                              Directory where created certificates will be saved. (Default: './certificates')
        -f OUT_FORMAT, --out_format OUT_FORMAT
                              .Output format ['jpg','png','bmp','pdf'] (Default: 'jpg')
        -i INTERVAL, --interval INTERVAL
                              Time interval(seconds) between consecutive mails. (Default: 2)
        -o, --overwrite       Whether to overwrite generated certificates if already exist. (Default: False)
        -c, --create_certificates_only
                              Only create certificates don't send. (Default: False)
        -v, --verbose         Whether vebose message are required. (Default: False)
        
- Example use:

      python certificate_mailer_app.py "certificate_mailer/data/test_data.csv" "EPAi2" "Rohan Shravan" 5000 "gaurav4664.test@gmail.com" -t "certificate_mailer/data/certi_template.jpg" -d "certificates" -f 'pdf' -i 2 -o
      
  Example use is illustrated in the aniation below.
  
  ![certificate_sender_app_gif](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/assets/certi_sender_app.gif)
  
  As shown above user can provide option as per her requirements. The app will ask for password for sender mail once. It will then create certificates for each of the students in the data file and send these certificates along with appropriate message and subject to the students.

- Valid data file format:

 The user data to be processed is provided to the app in the form of a csv file. User must keep in mind following points while creating the csv data file.
 1. Data file must have its first line as header. Data file without header will be rejected.
 2. Data file header must have atleast "Name","Score" and "Email" as fields. Data files without these fields will be rejeced.
 3. Data file must have appropriate number of data points in each row as there are fields in the header.
 4. Student name cannot have numeric or special characers.
 5. student score cannot be more than total score in the course
 6. Student email id must be valid email id.

##### User Defined templates:  

  This repo comes with a default certificate template [certi_template.jpg](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/certificate_mailer/data/certi_template.jpg). If user needs to use some other certificate template, she needs to provide a json file containing coordinates of different certificate fields. User can manually create this json file as shown in [certi_template.json](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/certificate_mailer/data/certi_template.json) default template file.

  User can use use [template_helper](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/template_helper.py) to generate template json file.

  Call template_helper

      python template_helper.py "template_file.jpg"      
      
 This will load a GUI with user defined template image. User must click points on the image as per instructions shown on the right side of the GUI. 
 points. The template_helper app will generate a json file with field coordinates. User must keep template image file and template json file in the same directory while using certificate_mailer app.
 
 Entire process is illustrated in the animation below. 


 ![template_helper_gif](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/assets/template_helper.gif)


### Under the hood  
Heart of the application lies in **'certificate_mailer'** package. It has 3 modules.

#### core  
This is the most important module. It contains functions responsible for creating certificates, mailing the certificates, iterator class for csv file etc. Some of the important functions are listed below.

1. CsvDataIterator class:

This class is responsible for iterating through csv file data. 

2. create_certificate(student_name:'str',course_name:'str',sign_name:'str',certi_template:'str',out_format:'str',certi_dir:'str',overwrite:'bool')

This function creates a certificate file using given *certi_template* as template for student with name *student_name* studying in *course_name* course being conducted by *sign_name* person. The certificate file has type *out_format*(.jpg,.bmp,.png,.pdf). It stores the certificate in *certi_dir* directory. If *overwrite* is True, certificate file will be overwritten if it already exists. 

3. mail_the_certificate(student_name:'str',student_score:'str',course_name:'str',total_marks:'float',sign_name:'str',certificate_path:'str',               receiver_email:'str',sender_email:'str',password:'obj',verbose:'bool')  

This function first creates email subject and email body for student *student_name* having score *student_score* studying in course *course_name* having total marks of *total_marks* and being conducted by *sign_name*. It then sends an email with this subject, body and certificate at *certificate_path* as attachment to *receiver_email*. It uses sender credentials (*sender_email*,*password*) for sending this mail. 

4. create_n_mail_certificates(csv_file_name:'str',course_name:'str',sign_name:'str',total_marks:'float', sender_email:'str',mail_interval:'int',certi_template:'str',certi_dir:'str',out_format:'str',overwrite:'bool',                    create_certi_only:'bool',verbose:'str')

This function combines *create_certificate* and *mail_the_certificate* functions. It iterates over *csv_file_name* creates certificate for each of the students and mails it to their email ids. It maintains time interval of *mail_interval* between consecutive emails.

#### mailer_utils

1. is_email_valid(email:'str')

This function checks email id for regex. It tells if email id is valid.

2. send_mail_with_attachment(subject:'str',body:'str',receiver_email:'str',sender_email:'str',password:'obj',                           attachment_file:'str',verbose:'bool')

This function composes an email with *subject*, *body* and *attachment_file* as attachment. It then sends it to *receiver_email*.

3. send_mail(subject:'str',body:'str',receiver_email:'str',sender_email:'str',password:'obj',verbose:'bool')    

This function composes an email with *subject* and *body*. It then sends it to *receiver_email*.

#### helpers

1. is_internet_connected():

This function checks if internet connection is available.

