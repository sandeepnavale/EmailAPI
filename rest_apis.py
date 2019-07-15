from EmailAPI import Email, SMTP_HOST, SMTP_PORT
from flask import Flask, request, abort

app = Flask(__name__)
app.config['MAIL_SERVER'] = SMTP_HOST
app.config['MAIL_PORT'] = SMTP_PORT
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


@app.route('/sendmail', methods=['POST'])
def index():
    if not request.json:
        abort(400)
    data = request.json
    eml = Email(data['service_provider'])
    ret = {}
    ret = eml.send_email(
        from_address=data['sender'],
        to_address=data['recipient'],
        subject=data['subject'],
        msg=data['body'],
    )
    print(ret)
    return f'Message send: {ret}', 201



@app.route('/sendmailaws', methods=['POST'])
def send_mailaws():
    if not request.json:
        abort(400)
    data = request.json
    eml = Email(data['service_provider'])
    ret = {}

    ret = eml.send_seperate_mail_aws(
        aws_smptp_host=data['aws_smptp_host'],
        aws_smptp_port=data['aws_smptp_port'],
        aws_smpt_user=data['aws_smpt_user'],
        aws_smpt_passwd=data['aws_smpt_passwd'],
        from_address=data['sender'],
        to_address=data['recipient'],
        subject=data['subject'],
        body=data['body'])
    print(ret)
    return f'AWS Message send: {ret}', 201

if __name__ == '__main__':
    app.run(debug=True)
