import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import csv

AWSSES = "AWSSES"
SENDGRID = "SENDGRID"
MAILGUN = "MAILGUN"
SMTP = "SMTP"
SMTP_HOST = "email-smtp.us-west-2.amazonaws.com"
SMTP_PORT = 587
with open('credentials.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    df = dict()
    for row in csv_reader:
        df["Smtp Username"] = row["Smtp Username"]
        df["Smtp Password"] = row["Smtp Password"]
        df['SENDGRID_API_KEY'] = row['SENDGRID_API_KEY']
        df['MAILGUN_API_KEY'] = row['MAILGUN_API_KEY']

# df = pd.read_csv('credentials.csv')
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
            self.user = df['Smtp Username']
            self.passwd = df['Smtp Password']
        elif srvs_provider == SENDGRID:
            self.__apikey = df['SENDGRID_API_KEY']
            self.client = SendGridAPIClient(self.__apikey)
            self.service_provider = SENDGRID
        elif srvs_provider == MAILGUN:
            self.service_provider = MAILGUN
            self.__apikey = df['MAILGUN_API_KEY']

        else:
            self.client = None

    def send_mailgun_email(self, from_address, to_address, subject, msg):
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
            server.login(df['Smtp Username'], df['Smtp Password'])
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
        return Mail(from_email=from_addr,
                    to_emails=to_addr,
                    subject=subject,
                    plain_text_content=body)

    def send_email(self,
                   from_address,
                   to_address,
                   subject="SUBJECT",
                   msg="BODY_TEXT"):
        status = 0
        try:
            if self.service_provider == SMTP:
                self.client.sendmail(self.user, to_address, msg)
            elif self.service_provider == SENDGRID:
                mail = self.compose_send_grid(from_address, to_address,
                                              subject, msg)
                response = self.client.send(mail)
                if response.status_code != 201:
                    status = False

            elif self.service_provider == AWSSES:
                status = self.send_aws_email(from_address, to_address, subject,
                                             msg)
                print(status)
            elif self.service_provider == MAILGUN:
                status = self.send_mailgun_email(from_address, to_address,
                                                 subject, msg)
        except Exception as e:
            print(e, status)
            return False
        finally:
            print('Email Sent')
        return False
