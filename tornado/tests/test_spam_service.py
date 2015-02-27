__author__ = 'himanshu'


import requests
import unittest

class TestSpamService(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/slow'


    def test_basic_non_spam(self):
        files = {'file': open('sample-nonspam.txt', 'rb')}
        r = requests.post(self.url, data=files['file'].read())
        self.assertEqual("HAM", r.text)

    def test_almost_non_spam(self):
        files = {'file': open('sample_almost_nonspam.txt', 'rb')}
        r = requests.post(self.url, data=files['file'].read())
        self.assertEqual("SPAM", r.text)

    def test_basic_spam(self):
        files = {'file': open('sample-spam.txt', 'rb')}
        r = requests.post(self.url, data=files['file'].read())
        self.assertEqual("SPAM", r.text)

    def test_other_spam(self):
        files = {'file': open('sample_spam.txt', 'rb')}
        r = requests.post(self.url, data=files['file'].read())
        self.assertEqual("SPAM", r.text)
    def test_non_spam_with_no_email_headers(self):
        files = {'file': open('non_spam_with_no_email_headers.txt', 'rb')}
        r = requests.post(self.url, data=files['file'].read())
        self.assertEqual("HAM", r.text)


if __name__ == '__main__':
    unittest.main()