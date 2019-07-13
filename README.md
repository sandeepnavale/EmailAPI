# EmailAPI
## Setup
1. EmailAPI.py contains basic functions to send emails.
2. rest_apis.py contains the restapi for sending email.
3. Chalice is used to deploy on AWS.
4. test_emails.py contains the unittests.

## Libraries used.
1. Chalice for deploying on AWS.
2. sendgrid, smtplib,requests, etc.

## Commands
### Chalice commands
1. pip install chalice -- to install chalice
chalice new-project -- to create new chalice project
chalice local -- to deploy services locally.
chalice deploy -- to deploy on AWS cloud

curl -X GET https://em6o892qgb.execute-api.us-west-2.amazonaws.com/api/sendmail


## Deployments
### Local deployment
1. Run rest_apis.py to get the local server. Ex:  http://127.0.0.1:5000/
2. In seperate terminal run below command to send the email.
curl -X POST \
  http://127.0.0.1:5000/sendmail \
  -H 'content-type: application/json' \
  -d '{
    "service_provider":"MAILGUN",
	"sender": "sandeepnl@outlook.com",
	"recipient": "mail2sandeepnl@gmail.com",
	"subject": "MAILGUN REST API Sender",
	"body": "<br><br> <b>Mail test</b>"
    }'

**Description of parameters.**
"service_provider" -- can be "MAILGUN", "AWSSES", or "SENDGRID",
"sender" -- From email address.  
"recipient"  -- To email address. 
"subject": -- Subject of email.
"body":  -- Body in a HTML format.
