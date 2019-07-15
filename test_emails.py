import unittest
import os
import subprocess

from rest_apis import app
from EmailAPI import Email


class MyTestDirectSendmail(unittest.TestCase):
    def test_send_via_aws_send_email(self):
        """ Test AWSSES Direct mail """
        eml = Email("AWSSES")
        ret = eml.send_email(
            from_address='sandeepnl@outlook.com',
            to_address='mail2sandeepnl@gmail.com',
            subject='AWS FUNC Test',
            msg=" AWS Func Test ",
        )
        self.assertFalse(ret)

    def test_send_via_sendgrid(self):
        """ Test Sendgrid """
        eml = Email("SENDGRID")
        status = eml.send_email(from_address='sandeepnl@outlook.com',
                                to_address='mail2sandeepnl@gmail.com',
                                subject='SendGrid Function test',
                                msg="SG Function test")
        self.assertFalse(status)

    def test_send_via_mailgun(self):
        """ Test mailgun """
        eml = Email("MAILGUN")
        status = eml.send_email(from_address='sandeepnl@outlook.com',
                                to_address='mail2sandeepnl@gmail.com',
                                subject='MailGun Function test',
                                msg="MailGun Function test")
        self.assertFalse(status)


class TestRestFunctions(unittest.TestCase):
    """ Test all local rest Apis """

    def cleanPorts(self):
        """ Clean up process & ports if its listening """
        cmd_output = " "
        try:
            cmd_output = subprocess.check_output('fuser 5000/tcp', shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output, e.returncode)
            cmd_output = " "
        if cmd_output is not " ":
            pid = int(cmd_output.strip())
            os.system('kill -9 ' + str(pid))

    def setUp(self):
        """ Change the working diretory to chalice directory, create process."""
        print(f'Current working directory is {subprocess.check_output("pwd")}')
        # os.chdir('AwsLambdaDeployment/serverlessDeployment')
        self.cleanPorts()
        self.proc1 = subprocess.Popen(
            [r'python', 'rest_apis.py', '--host', '127.0.0.1', '--port', '5000'],
            stdout=subprocess.PIPE,
            shell=True,
            preexec_fn=os.setsid)
        self.proc1.wait()
        print('Setup Done')

    def tearDown(self) -> None:
        """ Clean up ports & shutdown chalice process """
        print('Tearing down.')
        # os.chdir('..')
        self.cleanPorts()

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
                            "service_provider":
                            "MAILGUN",
                            "sender":
                            "sandeepnl@outlook.com",
                            "recipient":
                            "mail2sandeepnl@gmail.com",
                            "subject":
                            " MAILGUN REST API SEND TEST",
                            "body":
                            "<br><br> <b>MAILGUN REST API SEND TEST Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)


class TestCloudRestAPI(unittest.TestCase):
    """ Tests REST Api for AWS Lambda local & cloud """
    def cleanPorts(self):
        """ Clean up process & ports if its listening """
        cmd_output = " "
        try:
            cmd_output = subprocess.check_output('fuser 8000/tcp', shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output, e.returncode)
            cmd_output = " "
        if cmd_output is not " ":
            pid = int(cmd_output.strip())
            os.system('kill -9 ' + str(pid))

    def setUp(self):
        """ Change the working diretory to chalice directory, create process."""
        print(f'Current working directory is {subprocess.check_output("pwd")}')
        os.chdir('AwsLambdaDeployment/serverlessDeployment')
        self.cleanPorts()
        self.proc1 = subprocess.Popen(
            "chalice local --host 127.0.0.1 --port 8000",
            stdout=subprocess.PIPE,
            shell=True,
            preexec_fn=os.setsid)
        self.proc1.wait()
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
                            "service_provider":
                            "MAILGUN",
                            "sender":
                            "sandeepnl@outlook.com",
                            "recipient":
                            "mail2sandeepnl@gmail.com",
                            "subject":
                            " REST TESTING USING UNIT TEST",
                            "body":
                            "<br><br> <b>MAILGUN REST API SEND TEST Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)

    def test_mailgun_restapi_awssend(self):
        """ Tests send email via AWS SES services """
        with app.test_client() as c:
            rv = c.post('http://127.0.0.1:8000/sendmail',
                        json={
                            "service_provider":
                            "AWSSES",
                            "sender":
                            "sandeepnl@outlook.com",
                            "recipient":
                            "mail2sandeepnl@gmail.com",
                            "subject":
                            "AWSSES Cloud Unitest REST ",
                            "body":
                            "<br><br> <b> REST AWSSES From Unittest Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)

    def test_mailgun_restapi_sgsend(self):
        """ Tests send email via SENDGRID services """
        with app.test_client() as c:
            rv = c.post('http://127.0.0.1:8000/sendmail',
                        json={
                            "service_provider":
                            "SENDGRID",
                            "sender":
                            "sandeepnl@outlook.com",
                            "recipient":
                            "mail2sandeepnl@gmail.com",
                            "subject":
                            "SENDGRID Cloud Unittest REST ",
                            "body":
                            "<br><br> <b> REST AWSSES From Unittest Api </b>"
                        })

            print("RESPONSE CODE ", rv.status_code, " END ")
            self.assertEquals(rv.status_code, 201)


if __name__ == '__main__':
    unittest.main()
    # unittest.TestRestFunctions()
