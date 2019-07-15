import csv
import smtplib
import requests
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
with open('credentials.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    df = dict()
    for row in csv_reader:
        df["Smtp Username"] = row["Smtp Username"]
        df["Smtp Password"] = row["Smtp Password"]
        df['SENDGRID_API_KEY'] = row['SENDGRID_API_KEY']
        df['MAILGUN_API_KEY'] = row['MAILGUN_API_KEY']

AWS_REGION = 'us-west-2'


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

    def send_aws_email(self, from_address, to_address, subject, body):
        """ Sends the AWS Emails """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr((from_address, from_address))
        msg['To'] = to_address
        msg.add_header('Reply-To', from_address)

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
            server.sendmail(from_address, to_address, msg.as_string())
            server.close()
        except Exception as e:
            print(e)
            return True
        return False

    def send_email(self,
                   from_address="from@domain.com",
                   to_address='to@domain.com',
                   subject="Subject",
                   msg="Body text"):
        """ Meidiator function to send mails """
        status = 0
        try:
            if self.service_provider == SENDGRID:

                response = self.client.send(
                    Mail(from_email=from_address,
                         to_emails=to_address,
                         subject=subject,
                         plain_text_content=msg))
                if response.status_code != 202:
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

    def send_seperate_mail_aws(self,
                               aws_smptp_host="",
                               aws_smptp_port="",
                               aws_smpt_user="",
                               aws_smpt_passwd="",
                               from_address="from@domain.com",
                               to_address='to@domain.com',
                               subject="Subject",
                               body="Body text"):
        """ Sends the AWS Mails with Host, Port, SMTP User & Passwd inputs """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr((from_address, from_address))
        msg['To'] = to_address
        msg.add_header('Reply-To', from_address)

        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        try:
            server = smtplib.SMTP(aws_smptp_host, aws_smptp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(aws_smpt_user, aws_smpt_passwd)
            server.sendmail(from_address, to_address, msg.as_string())
            server.close()
        except Exception as e:
            print(e)
            return True
        return False

    def send_seperate_mail_aws(self,
                               aws_smptp_host="",
                               aws_smptp_port="",
                               aws_smpt_user="",
                               aws_smpt_passwd="",
                               from_address="from@domain.com",
                               to_address='to@domain.com',
                               subject="Subject",
                               body="Body text"):
        """ Sends the AWS Mails with Host, Port, SMTP User & Passwd inputs """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr((from_address, from_address))
        msg['To'] = to_address
        msg.add_header('Reply-To', from_address)

        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        try:
            server = smtplib.SMTP(aws_smptp_host, aws_smptp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(aws_smpt_user, aws_smpt_passwd)
            server.sendmail(from_address, to_address, msg.as_string())
            server.close()
        except Exception as e:
            print(e)
            return True
        return False


if __name__ == '__main__':
    eml = Email("AWSSES")
    status = eml.send_email(from_address='sandeepnl@outlook.com',
                            to_address='mail2sandeepnl@gmail.com',
                            subject='AWS Function test',
                            msg="AWS Function test")
