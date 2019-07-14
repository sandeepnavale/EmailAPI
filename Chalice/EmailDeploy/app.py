from chalice import Chalice
from EmailAPI import Email
from rest_apis import app
app = Chalice(app_name='EmailDeploy')


@app.route('/')
def index():
    return {'hello': 'world'}

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



