import unittest
import flask_restful
from rest_apis import app
from EmailAPI import Email


class MyTestCase(unittest.TestCase):
    def test_send_via_aws_send_email(self):
        eml = Email("AWS_SES")
        ret = eml.send_email(
            from_address='sandeepnl@outlook.com',
            to_address='mail2sandeepnl@gmail.com',
            subject='AWS FUNC Test',
            msg=" AWS Func Test ",
        )
        self.assertFalse(ret)

    def test_send_via_sendgrid(self):
        eml = Email("SEND_GRID")
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


if __name__ == '__main__':
    unittest.main()
