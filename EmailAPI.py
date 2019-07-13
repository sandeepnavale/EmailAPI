import os
import pathlib
import boto3
import email.utils
import smtplib
import sendgrid
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Email, Mail

AWSSES = "AWS_SES"
SENDGRID = "SEND_GRID"
MAILGUN = "MAIL_GUN"
SMTP = "SMTP"
SMTP_HOST = "email-smtp.us-west-2.amazonaws.com"
SMTP_PORT = 587

df = pd.read_csv('credentials.csv')
AWS_REGION = 'us-west-2'
# Mail contents
SENDER = 'sandeepnl@outlook.com'
SENDERNAME = 'Sandeep'
RECIPIENT = 'mail2sandeepnl@gmail.com'
SUBJECT = 'TEST SANDEEP'

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Hi Sandeep  This email was sent through your test program ")

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

body_subject = """"AWS SES Flask Mail Sender"""
body_simple = """<br><br> <b>Mail test</b>"""


class Email:
    def __init__(self, srvs_provider):
        if srvs_provider == SMTP:
            self.service_provider = SMTP
        elif srvs_provider == AWSSES:
            self.service_provider = AWSSES
            self.user = df['Smtp Username'][0]
            self.passwd = df['Smtp Password'][0]
            # self.init_smtp()
        elif srvs_provider == SENDGRID:
            self.__sg_apikey = df['SENDGRID_API_KEY'][0]
            self.client = SendGridAPIClient(self.__sg_apikey)
            self.service_provider = SENDGRID
        else:
            self.client = None



    def init_smtp(self):
        self.client = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        self.client.ehlo()
        self.client.starttls()
        self.client.ehlo()
        self.client.login(self.user, self.passwd, initial_response_ok=True)

    def compose_mime(self,
                     from_addr=SENDER,
                     to_addr=RECIPIENT,
                     subject=SUBJECT,
                     body=BODY_TEXT):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email.utils.formataddr((SENDERNAME, from_addr))
        msg['To'] = to_addr
        msg.add_header('Reply-To', from_addr)

        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')
        msg.attach(part1)
        msg.attach(part2)
        path = pathlib.Path.cwd().as_posix()
        filename = 'ML_Notation.pdf'
        file_path = path + '/' + filename
        attachment = open(file_path, "rb")
        part3 = MIMEBase('application', 'octet-stream')
        part3.set_payload(attachment.read())
        encoders.encode_base64(part3)
        part3.add_header('Content-Disposition',
                         "attachment; filename= %s" % filename)
        msg.attach(part3)

        return msg.as_string()

    def send_aws_email(self, reply_to, recipient, subject, body):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr((SENDERNAME, SENDER))
        msg['To'] = recipient
        msg.add_header('Reply-To', reply_to)

        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        try:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(df['Smtp Username'][0], df['Smtp Password'][0])
            server.sendmail(SENDER, recipient, msg.as_string())
            server.close()
        except Exception as e:
            print(e)

            return False
        else:
            return True

    def compose_send_grid(self,
                          from_addr=SENDER,
                          to_addr=RECIPIENT,
                          subject=SUBJECT,
                          body=BODY_TEXT):
        return Mail(from_email=from_addr,
                    to_emails=to_addr,
                    subject=subject,
                    plain_text_content=body)

    def send_email(self,
                   from_address,
                   to_address,
                   subject=SUBJECT,
                   msg=BODY_TEXT):
        status = 0
        try:
            if self.service_provider == SMTP:
                self.client.sendmail(self.user, to_address, msg)
            elif self.service_provider == SENDGRID:
                mail = self.compose_send_grid(from_address, to_address,
                                              subject, msg)
                response = self.client.send(mail)
                status = response.status_code
            elif self.service_provider == AWSSES:
                status = self.send_aws_email(from_address, to_address, subject, msg)

        except Exception as e:
            print(e)
        finally:
            print('Email Sent')
        return status

# #
# if __name__ == '__main__':
#     eml = Email("AWS_SES")
#     ret = eml.send_email(msg=" BODY_TEXT ",
#                          from_address='sandeepnl@outlook.com',
#                          to_address='mail2sandeepnl@gmail.com')
#     print(ret)
