# EPAi2 Capstone Project

## certificate_mailer  

This project implements a certificate generation and mailing app. User has to provide a csv file containing student data (name,score,email id etc). The app will generate a certificate for all the students using user selecteable certificate template and mail it to their respective email ids.

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


- User Defined templates:  

 This repo comes with a default certificate template [certi_template.jpg](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/certificate_mailer/data/certi_template.jpg). If user needs to use some other certificate template, she needs to provide a json file containing coordinates of different certificate fields. User can manually create this json file as shown in [certi_template.json](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/certificate_mailer/data/certi_template.json) default template file. 

 User can use use template_helper to generate template json file.

 Call template_helper

      python template_helper.py "template_file.jpg"      
      
 This will load a GUI with user defined template image. User must click points on the image as per instructions shown on the right side of the GUI. 
 points. The template_helper app will generate a json file with field coordinates. User must keep template image file and template json file in the same directory while using certificate_mailer app.
 
 Entire process is illustrated in the animation below. 


 ![template_helper_gif](https://github.com/GauravPatel89/EPAi2_capstone/blob/main/assets/template_helper.gif)

      

