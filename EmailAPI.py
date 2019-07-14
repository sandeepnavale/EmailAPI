import smtplib
import requests
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

AWSSES = "AWSSES"
SENDGRID = "SENDGRID"
MAILGUN = "MAILGUN"
SMTP = "SMTP"
SMTP_HOST = "email-smtp.us-west-2.amazonaws.com"
SMTP_PORT = 587

DF = pd.read_csv('credentials.csv')
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
            self.user = DF['Smtp Username'][0]
            self.passwd = DF['Smtp Password'][0]
        elif srvs_provider == SENDGRID:
            self.__apikey = DF['SENDGRID_API_KEY'][0]
            self.client = SendGridAPIClient(self.__apikey)
            self.service_provider = SENDGRID
        elif srvs_provider == MAILGUN:
            self.service_provider = MAILGUN
            self.__apikey = DF['MAILGUN_API_KEY'][0]
        else:
            self.client = None

    def send_mailgun_email(self, from_address, to_address, subject, msg):
        """ Sends the MailGun emails """
        status = requests.post(
            "https://api.mailgun.net/v3/sandboxff066e78a0f1460a8564a6e2d8566257.mailgun.org/messages",
            auth=("api", self.__apikey),
            data={
                "from": from_address,
                "to": to_address,
                "subject": subject,
                "text": msg
            })
        if status.status_code != 200:
            return True

        return False

    def send_aws_email(self, reply_to, recipient, subject, body):
        """ Sends the AWS Emails """
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
            server.login(DF['Smtp Username'][0], DF['Smtp Password'][0])
            server.sendmail(SENDER, recipient, msg.as_string())
            server.close()
        except Exception as e:
            print(e)
            return True
        return False

    def compose_send_grid(self,
                          from_addr=SENDER,
                          to_addr=RECIPIENT,
                          subject="SUBJECT",
                          body="BODY_TEXT"):
        """ Sends the sendgrid emails. """
        return Mail(from_email=from_addr,
                    to_emails=to_addr,
                    subject=subject,
                    plain_text_content=body)

    def send_email(self,
                   from_address,
                   to_address,
                   subject="SUBJECT",
                   msg="BODY_TEXT"):
        """ Meidiator function to send mails """
        status = 0
        try:
            if self.service_provider == SENDGRID:
                mail = 

                response = self.client.send(
                    Mail(from_email=from_address,
                            to_emails=to_address,
                            subject=subject,
                            plain_text_content=msg))
                if response.status_code != 201:
                    status = response.status_code
                    return True

            elif self.service_provider == AWSSES:
                status = self.send_aws_email(from_address, to_address, subject,
                                             msg)
                print(status)
            elif self.service_provider == MAILGUN:
                status = self.send_mailgun_email(from_address, to_address,
                                                 subject, msg)
        except Exception as e:
            print('ERROR IN SENDING EMAIL ', e, status)
            return True
        finally:
            print('Email Sent -- SUCCESS')
        return False
