from chalice import Chalice
from EmailAPI import Email
from rest_apis import app
app = Chalice(app_name='serverlessDeployment')
app.debug = True

@app.route('/')
def index():
    return {'hello': 'SandeepNL'}


@app.route('/sendmail', methods=['POST'])
def sendmail():
    data = app.current_request.json_body
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
def sendmailaws():
    data = app.current_request.json_body
    eml = Email(data['service_provider'])
    ret = {}
    ret = eml.send_email(
        aws_smptp_host=data['aws_smptp_host'],
        aws_smptp_port=data['aws_smptp_port'],
        aws_smpt_user=data['aws_smpt_user'],
        aws_smpt_passwd=data['aws_smpt_passwd'],
        from_address=data['sender'],
        to_address=data['recipient'],
        subject=data['subject'],
        msg=data['body'],
    )
    print(ret)
    return f'Message AWS Mail send: {ret}', 201
