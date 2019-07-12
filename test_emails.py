import unittest
from EmailAPI import Email

class MyTestCase(unittest.TestCase):
    def test_send_via_awsses(self):
        eml = Email("AWS_SES")
        txt = eml.compose_email()
        eml.send_email(msg=txt, to_address='mail2sandeepnl@gmail.com')

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
