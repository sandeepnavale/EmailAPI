import unittest
from EmailAPI import Email

BODY_TEXT = ("Hi Sandeep \r\n"
             "This email was sent through your test program ")

class MyTestCase(unittest.TestCase):
    def test_send_via_aws_send_email(self):
        eml = Email("AWS_SES")
        ret = {}
        ret = eml.send_email(msg=BODY_TEXT, from_address='sandeepnl@outlook.com', to_address='mail2sandeepnl@gmail.com')
        self.assertEqual(len(ret), 0)

    def test_send_via_sg_send_email(self):
        eml = Email("SEND_GRID")
        status = eml.send_email(msg=BODY_TEXT,from_address='sandeepnl@outlook.com',to_address='mail2sandeepnl@gmail.com')
        self.assertEqual(status,202)


if __name__ == '__main__':
    unittest.main()
