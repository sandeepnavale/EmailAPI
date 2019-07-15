import unittest
import os
import subprocess

from rest_apis import app
from EmailAPI import Email


class MyTestCase(unittest.TestCase):
    def test_send_via_aws_send_email(self):
        eml = Email("AWSSES")
        ret = eml.send_email(
            from_address='sandeepnl@outlook.com',
            to_address='mail2sandeepnl@gmail.com',
            subject='AWS FUNC Test',
            msg=" AWS Func Test ",
        )
        self.assertFalse(ret)

    def test_send_via_sendgrid(self):
        eml = Email("SENDGRID")
        status = eml.send_email(from_address='sandeepnl@outlook.com',
                                to_address='mail2sandeepnl@gmail.com',
                                subject='SendGrid Function test',
                                msg="SG Function test")
        self.assertFalse(status)

    def test_send_via_mailgun(self):
        eml = Email("MAILGUN")
        status = eml.send_email(from_address='sandeepnl@outlook.com',
                                to_address='mail2sandeepnl@gmail.com',
                                subject='MailGun Function test',
                                msg="MailGun Function test")
        self.assertFalse(status)


class TestRestFunctions(unittest.TestCase):
    def test_sendgrid_restapi(self):
        """ Tests send email via SendGrid services """
        with app.test_client() as c:
            rv = c.post('/sendmail',
                        json={
                            "service_provider": "SENDGRID",
                            "sender": "sandeepnl@outlook.com",
                            "recipient": "mail2sandeepnl@gmail.com",
                            "subject": " REST API testing for SendGrid ",
                            "body": "<br><br> <b>Mail test</b>"
                        })
            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)

    def test_awsses_restapi(self):
        """ Tests send email via AWS SES services """
        with app.test_client() as c:
            rv = c.post('/sendmail',
                        json={
                            "service_provider": "AWSSES",
                            "sender": "sandeepnl@outlook.com",
                            "recipient": "mail2sandeepnl@gmail.com",
                            "subject": " AWS REST API TEST",
                            "body": "<br><br> <b>Testing AWS SES REST Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)

    def test_mailgun_restapi_send(self):
        """ Tests send email via AWS SES services """
        with app.test_client() as c:
            rv = c.post('/sendmail',
                        json={
                            "service_provider": "MAILGUN",
                            "sender": "sandeepnl@outlook.com",
                            "recipient": "mail2sandeepnl@gmail.com",
                            "subject": " MAILGUN REST API SEND TEST",
                            "body": "<br><br> <b>MAILGUN REST API SEND TEST Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)


class TestCloudRestAPI(unittest.TestCase):

    def cleanPorts(self):
        CmdOutput = " "
        try:
            CmdOutput = subprocess.check_output('fuser 8000/tcp', shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output, e.returncode)
            CmdOutput = " "
        if CmdOutput is not " ":
            port = int(CmdOutput.strip())
            os.system('kill -9 ' + str(port))

    def setUp(self):
        """ Change the working diretory to chalice directory, create process."""
        print(f'Current working directory is {subprocess.check_output("pwd")}')
        os.chdir('AwsLambdaDeployment/serverlessDeployment')
        self.cleanPorts()
        self.proc1 = subprocess.Popen("chalice local --host 127.0.0.1 --port 8000", stdout=subprocess.PIPE,
                                      shell=True, preexec_fn=os.setsid)

        print('Setup Done')

    def tearDown(self) -> None:
        """ Clean up ports & shutdown chalice process """
        print('Tearing down.')
        os.chdir('../../')
        self.cleanPorts()

    def test_mailgun_restapi_mailgunsend(self):
        """ Tests send email via MAILGUN services """
        with app.test_client() as c:
            rv = c.post('http://127.0.0.1:8000/sendmail',
                        json={
                            "service_provider": "MAILGUN",
                            "sender": "sandeepnl@outlook.com",
                            "recipient": "mail2sandeepnl@gmail.com",
                            "subject": " REST TESTING USING UNIT TEST",
                            "body": "<br><br> <b>MAILGUN REST API SEND TEST Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)


    def test_mailgun_restapi_awssend(self):
        """ Tests send email via AWS SES services """
        with app.test_client() as c:
            rv = c.post('http://127.0.0.1:8000/sendmail',
                        json={
                            "service_provider": "AWSSES",
                            "sender": "sandeepnl@outlook.com",
                            "recipient": "mail2sandeepnl@gmail.com",
                            "subject": "AWSSES Cloud Unitest REST ",
                            "body": "<br><br> <b> REST AWSSES From Unittest Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)


    def test_mailgun_restapi_sgsend(self):
        """ Tests send email via SENDGRID services """
        with app.test_client() as c:
            rv = c.post('http://127.0.0.1:8000/sendmail',
                        json={
                            "service_provider": "SENDGRID",
                            "sender": "sandeepnl@outlook.com",
                            "recipient": "mail2sandeepnl@gmail.com",
                            "subject": "SENDGRID Cloud Unittest REST ",
                            "body": "<br><br> <b> REST AWSSES From Unittest Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)

if __name__ == '__main__':
    unittest.main()
    # os.chdir('AwsLambdaDeployment/serverlessDeployment')