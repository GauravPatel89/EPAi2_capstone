import argparse
import certificate_mailer

def main(args):
    """
    This function implements certificate mailing application using certificate_mailer package

    Parameters:
        args(argparse obj): argparse object containing arguments passed by the user.

    Returns:
        None
    """
    try:
        if args.verbose:
            print('Arguments passed',args)

        # Call create_n_mail_certificates function with proper arguments
        if certificate_mailer.create_n_mail_certificates(
            csv_file_name = args.csv_file,course_name = args.course_name,
            sign_name = args.sign_name, total_marks = args.total_marks,
            sender_email = args.sender_email, mail_interval = args.interval,
            certi_template = args.certi_template, certi_dir = args.certi_dir,
            out_format = args.out_format,overwrite = args.overwrite,
            create_certi_only = args.create_certificates_only,verbose = args.verbose):
            print('-'*30)
            print('Success!!!')
        else:
            print('-'*30)
            print('Failed!!!')
    except Exception as e:
        print(e)
        print('-'*30)
        print('Failed!!!')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("csv_file",type=str, help="csv file containing the student data")

    parser.add_argument("course_name",type=str, help="Name of the course")

    parser.add_argument("sign_name",type=str, help="Signature name to be printed on certificate")

    parser.add_argument("total_marks",type=float, help="Total marks in the course")

    parser.add_argument("sender_email",type=str, help="Email id of sender. Password will be asked later")

    parser.add_argument("-t","--certi_template",type=str,default='./certificate_mailer/data/certi_template.jpg',help="Path where created certificates will be saved. (Default: %(default)r)")    

    parser.add_argument("-d","--certi_dir",type=str,default='./certificates',help="Directory where created certificates will be saved. (Default: %(default)r)")

    parser.add_argument("-f","--out_format",type=str,default='jpg',help=".Output format ['jpg','png','bmp','pdf'] (Default: %(default)r)")

    parser.add_argument("-i","--interval",type=float,default=2,help="Time interval(seconds) between consecutive mails. (Default: %(default)r)")

    parser.add_argument("-o","--overwrite",action="store_true",default=False,help="Whether to overwrite generated certificates if already exist. (Default: %(default)r)")

    parser.add_argument("-c","--create_certificates_only",action="store_true",default=False,help="Only create certificates don't send. (Default: %(default)r)")

    parser.add_argument("-v", "--verbose", action="store_true", default=False,help= "Whether vebose message are required. (Default: %(default)r)")

    args = parser.parse_args()
    main(args)