import os
import boto3
import email.utils
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# from botocore.exceptions import ClientError


from sendgrid import SendGridAPIClient

# from sendgrid.helpers.mail import Mail


AWSSES = "AWS_SES"
SENDGRID = "SEND_GRID"
MAILGUN = "MAIL_GUN"
SMTP = "SMTP"
SMTP_HOST = "email-smtp.us-west-2.amazonaws.com"
SMTP_PORT = 25  # 587
SMTP_USER = 'AKIA5QG7FCPYM2TG2XHK'
SMTP_PASSWD = 'BPRDpFyPTfCP/YQSABmu2B5wSROPQ9C33XTcXWoJ50E2'
AWS_REGION = 'us-west-2'
USER = 'user'
PASSWD = 'passwd'

# Mail contents
SENDER = 'sandeepnl@outlook.com'
SENDERNAME = 'Sandeep N L'
RECIPIENT = 'mail2sandeepnl@gmail.com'
SUBJECT = 'TEST SES SANDEEP'

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Hi Sandeep \r\n"
             "This email was sent through your test program "
             )

BODY_HTML = """<html>
<head></head>
<body>
  <h1>TESTING SANDEEP </h1>
  <p>This email was sent with Amazon SES using the 
    <a href='https://www.python.org/'>Python</a>
    <a href='https://docs.python.org/3/library/smtplib.html'>
    smtplib</a> library.</p>
    <p> GOOD LUCK SANDEEP </p>
</body>
</html>
            """


class Email:
    def __init__(self, srvs_provider):

        if srvs_provider == SMTP:
            self.service_provider = SMTP
         elif srvs_provider == AWSSES:
            self.service_provider = AWSSES
            # self.client = boto3.client('ses', region_name=AWS_REGION)
            self.user = SMTP_USER
            self.passwd = SMTP_PASSWD

        elif srvs_provider == SENDGRID:
            self.client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        else:
            self.client = None

        self.init_smtp()

    def init_smtp(self):
        # self.client = smtplib.SMTP('smtp.office365.com', 587)
        self.client = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        self.client.ehlo()
        self.client.starttls()
        # self.client.ehlo
        self.client.login(self.user, self.passwd, initial_response_ok=True)

    def compose_email(self, from_addr=SENDER, to_addr=RECIPIENT, subject=SUBJECT, body=BODY_TEXT):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email.utils.formataddr((SENDERNAME,from_addr ))
        msg['To'] = to_addr
        part1 = MIMEText(body, 'plain')
        # part2 = MIMEText(BODY_HTML, 'html')
        msg.attach(part1)
        # msg.attach(part2)

        filename = 'DataEngineer.pdf'
        path = '/home/sandeepnl/' + filename
        attachment = open(path, "rb")
        part3 = MIMEBase('application', 'octet-stream')
        part3.set_payload(attachment.read())
        encoders.encode_base64(part3)
        part3.add_header('Content-Disposition',
                         "attachment; filename= %s" % filename)
        msg.attach(part3)

        return msg.as_string()

    def send_email(self, from_address, to_address, msg):
        try:
            if self.service_provider == SMTP:
                self.client.sendmail(self.user, to_address, msg)
            elif self.service_provider == SENDGRID:
                response = self.client.send(msg)
                print(response.status_code)
                # print(response.body)
                # print(response.headers)
            elif self.service_provider == AWSSES:
                self.client.sendmail('sandeepnl@outlook.com', to_address, msg)

        except Exception as e:
            print(e)

    def receive_email(self):
        """ NOT ASKED -- If IMAP / POP for this task. """
        pass


if __name__ == '__main__':
    eml = Email(AWSSES)
    txt = eml.compose_email()
    eml.send_email(msg=txt, to_address='mail2sandeepnl@gmail.com')
