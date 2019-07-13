import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from EmailAPI import Email
from flask import Flask, request, abort

app = Flask(__name__)
app.config['MAIL_SERVER']='email-smtp.us-west-2.amazonaws.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL']= False
app.config['MAIL_USERNAME'] = 'EMAIL_ID'
app.config['MAIL_PASSWORD'] = 'PASSWORD'


# Email
SENDER = 'sandeepnl@outlook.com'
SENDERNAME = 'Sandeep NL'
USERNAME_SMTP = "AKIA5QG7FCPYM2TG2XHK"
PASSWORD_SMTP = "BPRDpFyPTfCP/YQSABmu2B5wSROPQ9C33XTcXWoJ50E2"
HOST = "email-smtp.us-west-2.amazonaws.com"
PORT = 587
#
#
# def send_email(reply_to, recipient, subject, body):
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = subject
#     msg['From'] = formataddr((SENDERNAME, SENDER))
#     msg['To'] = recipient
#     msg.add_header('Reply-To', reply_to)
#
#     part1 = MIMEText(body, 'plain')
#     part2 = MIMEText(body, 'html')
#     msg.attach(part1)
#     msg.attach(part2)
#
#     try:
#         server = smtplib.SMTP(HOST, PORT)
#         server.ehlo()
#         server.starttls()
#         server.ehlo()
#         server.login(USERNAME_SMTP, PASSWORD_SMTP)
#         server.sendmail(SENDER, recipient, msg.as_string())
#         server.close()
#     except Exception as e:
#         return False
#     else:
#         return True


@app.route('/', methods=['POST'])
def index():
    if not request.json:
        abort(400)
    data = request.json

    eml = Email(data['service_provider'])
    ret = {}
    ret = eml.send_email(from_address=data['sender'],
                         to_address=data['recipient'],
                         subject=data['subject'],
                         msg=data['body'],
                         )

    return f'Message send: {ret}', 201

if __name__ == '__main__':
    app.run(debug=True)